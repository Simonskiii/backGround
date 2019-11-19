from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.backends import ModelBackend

from users.tasks import send_register_email
from utils.baseResponse import baseResponse
from utils.email_send import random_str
from .models import UserProfile
from django.db.models import Q
from django.views.generic.base import View
from .forms import LoginForm, RegisterForm

from rest_framework.mixins import CreateModelMixin, ListModelMixin, UpdateModelMixin
from rest_framework.response import Response
from random import choice
from rest_framework import mixins, viewsets, status, permissions, authentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .models import VerifyCode
from .serializers import SmsSerializer, EmailSerializer, UserRegSerializer, UserDetailSerializer, UserProfileSerializer

# Create your views here.

User = get_user_model()


class UserProfileViewset(viewsets.GenericViewSet, UpdateModelMixin, ListModelMixin):
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        return User.objects.filter(username=self.request.user)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(baseResponse(success="更改成功"))


class UserViewSet(CreateModelMixin, viewsets.GenericViewSet, ListModelMixin):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return UserDetailSerializer
        elif self.action == "create":
            return UserRegSerializer

        return UserDetailSerializer

    # permission_classes = (permissions.IsAuthenticated, )
    def get_permissions(self):
        if self.action == "retrieve":
            return [permissions.IsAuthenticated()]
        elif self.action == "create":
            return []

        return []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        re_dict = serializer.data
        # payload = jwt_payload_handler(user)
        # re_dict["token"] = jwt_encode_handler(payload)
        name = user.name if user.name else user.username

        headers = self.get_success_headers(serializer.data)
        return Response(baseResponse(success="注册成功"), status=status.HTTP_201_CREATED, headers=headers)

    def get_object(self):
        return self.request.user

    def perform_create(self, serializer):
        return serializer.save()


class RegisterViewset(CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = EmailSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        email_record = VerifyCode()
        code = random_str(6)
        email_record.code = code
        email_record.email = email
        email_record.send_type = "register"

        send_status = send_register_email.delay(email, code)

        if send_status:
            email_record.save()
            return Response(baseResponse(success="验证码已发送"), status=status.HTTP_201_CREATED)
        else:
            return Response(baseResponse(error="发送失败"), status=status.HTTP_400_BAD_REQUEST)


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm(request.POST)
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST['email']
            pass_word = request.POST['password']
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.password = make_password(password=pass_word)
            user_profile.save()
            send_register_email.delay(user_name, 'register')
            return render(request, 'login.html')
        return render(request, 'register.html', {'register_form': register_form})


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html', {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST['username']
            pass_word = request.POST['password']
            user = authenticate(request, username=user_name, password=pass_word)
            if user is not None:
                login(request, user)
                return render(request, 'index.html', {'username': user})
            else:
                return render(request, 'login.html', {'msg': '用户名或密码错误'})
        else:
            return render(request, 'login.html', {'login_form': login_form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return render(request, 'index.html', {})


def user_login(request):
    if request.method == 'POST':
        user_name = request.POST['username']
        pass_word = request.POST['password']
        user = authenticate(request, username=user_name, password=pass_word)
        if user is not None:
            login(request, user)
            return render(request, 'index.html', {'username': user})
        else:
            return render(request, 'login.html', {'msg': '用户名或密码错误'})
    elif request.method == 'GET':
        return render(request, 'login.html', {})


class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception:
            return None


class SmsCodeViewset(CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = SmsSerializer

    def generate_code(self):
        """
        生成四位数字的验证码
        :return:
        """
        seeds = "1234567890"
        random_str = []
        for i in range(4):
            random_str.append(choice(seeds))

        return "".join(random_str)

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #
    #     mobile = serializer.validated_data["mobile"]
    #     yun_pian = YunPian(APIKEY)
    #
    #     code = self.generate_code()
    #
    #     sms_status = yun_pian.send_sms(code=code, mobile=mobile)
    #
    #     if sms_status["code"] != 0:
    #         return Response({
    #             "mobile": sms_status["msg"]
    #         }, status=status.HTTP_400_BAD_REQUEST)
    #     else:
    #         code_record = VerifyCode(code=code, mobile=mobile)
    #         code_record.save()
    #         return Response({
    #             "mobile": mobile
    #         }, status=status.HTTP_201_CREATED)

# class UserViewset(CreateModelMixin, viewsets.GenericViewSet):
