from rest_framework import serializers, status
from django.contrib.auth import get_user_model
import re
from rest_framework.validators import UniqueValidator, UniqueForDateValidator
import pytz
from backGround.settings import REGEX_MOBILE, REGEX_EMAIL
import datetime

from users.mUniqueValidator import mValidationError
from utils.baseResponse import baseResponse
from .models import VerifyCode

User = get_user_model()


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("name", "gender", "birthday", "mobile", 'id')


class UserDetailSerializer(serializers.ModelSerializer):
    """
    用户详情序列化类
    """

    class Meta:
        model = User
        fields = ("name", "gender", "birthday", "email", "mobile", 'id')


# 验证码
class EmailSerializer(serializers.Serializer):
    email = serializers.CharField(label="邮箱", required=True, allow_blank=False,
                                  max_length=50, )

    # username = serializers.CharField(label="用户名", help_text="用户名", required=True, allow_blank=False,
    #                                  validators=[UniqueValidator(queryset=User.objects.all(), message="用户已经存在"),
    #                                              UniqueValidator(queryset=VerifyCode.objects.values("email"),
    #                                                              message="发过了")],
    #                                  max_length=30)
    # password = serializers.CharField(
    #     style={'input_type': 'password'}, help_text="密码", label="密码", write_only=True,
    # )

    def validate_email(self, email):
        minutes_ago = datetime.datetime.now() - datetime.timedelta(hours=0, minutes=10, seconds=0)
        hours_ago = datetime.datetime.now() - datetime.timedelta(hours=0, minutes=30, seconds=0)
        if VerifyCode.objects.filter(add_time__gt=minutes_ago, email=email).count():
            raise mValidationError(detail=baseResponse(error="距离上一次发送未超过10min"))
        # 删除一个小时之前的数据
        VerifyCode.objects.filter(add_time__lt=hours_ago).delete()

        if User.objects.filter(email=email).count():
            raise mValidationError(detail=baseResponse(error="邮箱已注册"))
        if not re.match(REGEX_EMAIL, email):
            raise mValidationError(detail=baseResponse(error="邮箱不合法"))

        return email


class SmsSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11)

    def validate_mobile(self, mobile):
        """
        验证手机号码
        :param mobile:
        :return:
        """
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError('用户已存在')

        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError('手机号码不合法')
        one_minutes_ago = datetime.datetime.now() - datetime.timedelta(hours=0, minutes=1, seconds=0)
        if VerifyCode.objects.filter(add_time__gt=one_minutes_ago, mobile=mobile).count():
            raise serializers.ValidationError("距离上一次发送未超过60s")
        return mobile


# 注册Serializer
class UserRegSerializer(serializers.ModelSerializer):
    code = serializers.CharField(required=True, write_only=True, max_length=20, min_length=4, help_text='验证码',
                                 error_messages={
                                     'blank': '请输入验证码', 'required': '不能为空', 'max_length': '验证码没这么长',
                                     'min_length': '验证码没这么短'
                                 })
    name = serializers.CharField(label="用户名", help_text="用户名", required=True, allow_blank=False,
                                 max_length=30)
    password = serializers.CharField(
        style={'input_type': 'password'}, help_text="密码", label="密码", write_only=True,
    )
    email = serializers.CharField(label="邮箱", help_text="邮箱", required=True, allow_blank=False,
                                  max_length=30)

    def validate_email(self, email):
        if User.objects.filter(email=email).count():
            raise mValidationError(detail=baseResponse(error="邮箱已注册"))
        return email

    # def validate_name(self, name):
    #     if User.objects.filter(name=name).count():
    #         raise mValidationError(detail=baseResponse(error="用户名已注册"))
    #     return name

    def create(self, validated_data):
        user = super(UserRegSerializer, self).create(validated_data=validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    # 验证验证码错没错
    def validate_code(self, code):
        verify_recodes = VerifyCode.objects.filter(email=self.initial_data['email']).order_by("-add_time")
        if verify_recodes:
            last_record = verify_recodes.first()
            minutes_ago = datetime.datetime.now() - datetime.timedelta(hours=0, minutes=30, seconds=0)
            minutes_ago = minutes_ago.replace(tzinfo=pytz.timezone('UTC'))
            if minutes_ago > last_record.add_time:
                VerifyCode.objects.filter(add_time__lt=minutes_ago).delete()
                raise mValidationError(detail=baseResponse(error="验证码过期"))
            if last_record.code != code:
                raise mValidationError(detail=baseResponse(error="验证码错误"))
        else:
            raise mValidationError(detail=baseResponse(error="验证码错误"))

    # 删除用不到的字段code
    def validate(self, attrs):
        attrs['username'] = attrs['email']
        del attrs['code']
        return attrs

    class Meta:
        model = User
        fields = ('name', 'password', 'email', 'code')
