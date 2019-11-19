from django.db import models
from datetime import datetime
from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model
import factory
from faker import Factory
User = get_user_model()
fake = Factory.create()
# Create your models here.


class ArticleCatergory(models.Model):
    name = models.CharField(default="", max_length=30, verbose_name="类别名", help_text="类别名")
    code = models.CharField(default="", max_length=30, verbose_name="类别code", help_text="类别code")
    parent_category = models.ForeignKey("self", null=True, blank=True, verbose_name="父类目级别", help_text="父目录",
                                        related_name="sub_cat", on_delete=models.CASCADE)
    is_tab = models.BooleanField(default=False, verbose_name="是否导航", help_text="是否导航")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "商品类别"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Article(models.Model):
    name = models.CharField(default='', max_length=50, verbose_name='题目', help_text='题目', null=True)
    category = models.ForeignKey(ArticleCatergory, verbose_name='文章类别', on_delete=models.CASCADE, default='')
    content = RichTextField('文章内容')
    click_num = models.IntegerField(default=0, verbose_name='点击数')
    fav_num = models.IntegerField(default=0, verbose_name='喜欢数')
    aritcle_brief = models.TextField(max_length=500, verbose_name="文章概述", default='')
    article_front_image = models.ImageField(upload_to="article/images/", null=True, blank=True, verbose_name="封面图")
    is_hot = models.BooleanField(default=False, verbose_name="是否热门")
    is_anonymous = models.BooleanField(default=False, verbose_name='是否匿名')
    # author = models.ForeignKey(User, verbose_name='作者', on_delete=models.SET_DEFAULT, default='')
    author = models.CharField(max_length=20, default='', verbose_name='作者', help_text='作者')

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class ArticleShow(models.Model):
    name = models.ForeignKey(Article, on_delete=models.SET_DEFAULT, verbose_name='文章名', help_text='文章名', default='')
    User = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户', help_text='用户', default='')


class ArticleImage(models.Model):
    """
    商品轮播图
    """
    articles = models.ForeignKey(Article, verbose_name="文章", related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="", verbose_name="图片", null=True, blank=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = '封面图'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.articles.name


# import random
# class ArticleCatergoryFactory(factory.DjangoModelFactory):
#     class Meta:
#         model = ArticleCatergory
#     name = fake.word()
#     li = []
#     for i in name.split(" "):
#         li.append(i[0])
#     code = "".join('1')
#     catergory_type = random.randint(1,3)
#
#
# class ArticleFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = Article
#     author = fake.name()
#     content = fake.text()
#     name = fake.word()
#     category = factory.SubFactory(ArticleCatergoryFactory)



