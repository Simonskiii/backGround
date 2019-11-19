from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework import serializers
from django.db.models import Q
from articles import models
from users.mUniqueValidator import mValidationError
from utils.baseResponse import baseResponse
from .models import Article, ArticleCatergory, ArticleShow
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField


class IsActiveListSerializer(serializers.ListSerializer):

    def to_representation(self, data):
        following = [1, 2, 3]
        data = data.order_by('click_num')[:3]
        # data = data.filter(id__in=[f for f in following])
        return super().to_representation(data)


class AritcleShowSerializer(ModelSerializer):
    usagedata = serializers.SerializerMethodField()

    class Meta:
        model = ArticleShow
        fields = '__all__'
        list_serializer_class = IsActiveListSerializer

    def get_usagedata(self, obj):
        return models.Article.objects.filter(name='media').count()


class AriticleCreateSerializer(Serializer):
    name = serializers.CharField(max_length=20, required=True, help_text='题目')
    category = serializers.PrimaryKeyRelatedField(queryset=ArticleCatergory.objects.all())
    content = serializers.CharField(required=True, help_text='内容')

    def validate_name(self, name):
        if Article.objects.filter(name=name).count():
            raise mValidationError(detail=baseResponse(error="文章已存在"))
        return name

    def create(self, validated_data):
        a = Article(**validated_data)
        return a
