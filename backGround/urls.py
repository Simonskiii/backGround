"""backGround URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from . import settings
from goods.views import GoodsListViewset, CategoryViewset, getform
from users.views import UserViewSet, RegisterViewset, UserProfileViewset
from articles.views import ArticleViewset
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

router = DefaultRouter()

router.register(r'goods', GoodsListViewset, base_name='goods')
router.register(r'categories', CategoryViewset, base_name='categories')
router.register(r'articles', ArticleViewset, base_name='articles')
router.register(r'user', UserViewSet, base_name='user')
router.register(r'verify', RegisterViewset, base_name='verify')
router.register(r'profile', UserProfileViewset, base_name='profile')

urlpatterns = [
    re_path(r'media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    path('admin/', admin.site.urls),
    path(r'api-token-auth/', views.obtain_auth_token),
    path(r'jwt-token-auth/', obtain_jwt_token),
    path(r'jwt-token-refresh/', refresh_jwt_token),
    path('g/', include(router.urls)),
]
