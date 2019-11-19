from django.contrib import admin
from .models import Article, ArticleCatergory, ArticleImage

# Register your models here.


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['name', 'content', 'category', 'author', 'click_num', 'fav_num', 'is_hot']
    search_fields = ['name', 'author']
    list_editable = ['is_hot']
    list_filter = ['category', 'author', ]
    style_fields = {"content": "RichTextField"}

    class ArticlesImagesInline(admin.TabularInline):
        model = ArticleImage
        exclude = ["add_time"]
        extra = 1
        style = 'tab'

    inlines = [ArticlesImagesInline]


class ArticleCatergoryAdmin(admin.ModelAdmin):
    list_display = ['code', 'name',  'parent_category', ]
    search_fields = ['name', 'node']
    list_filter = ['name']


admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleCatergory, ArticleCatergoryAdmin)
