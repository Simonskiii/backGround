from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet

from utils.baseResponse import baseResponse
from .models import Article, ArticleCatergory
from rest_framework import status
from .serializers import AritcleShowSerializer, AriticleCreateSerializer
import json
# Create your views here.


class ArticleViewset(CreateModelMixin, GenericViewSet, ListModelMixin, RetrieveModelMixin, UpdateModelMixin):
    queryset = Article.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return AritcleShowSerializer
        elif self.action == 'create':
            return AriticleCreateSerializer
        else:
            return AritcleShowSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(baseResponse(data=serializer.data))

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(baseResponse(success="文章发表成功"), status=status.HTTP_201_CREATED, headers=headers)
