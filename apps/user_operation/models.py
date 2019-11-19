from django.db import models
from django.contrib.auth import get_user_model
from articles.models import Article, ArticleCatergory

User = get_user_model()


# Create your models here.


class UserReadAricle(models.Model):
    user = models.ForeignKey(User, verbose_name="用户名", on_delete=models.CASCADE)
    article = models.ForeignKey(Article, verbose_name='文章题目', on_delete=models.CASCADE)
    category = models.ForeignKey(ArticleCatergory, verbose_name='文章类别', on_delete=models.CASCADE)


# class UserFavAricle(models.Model):
#     user = models.ForeignKey(User, verbose_name="用户名", on_delete=models.CASCADE)
#     article = models.ForeignKey(Article, verbose_name='文章题目', on_delete=models.CASCADE)
#     category = models.ForeignKey(ArticleCatergory, verbose_name='文章类别', on_delete=models.CASCADE)
