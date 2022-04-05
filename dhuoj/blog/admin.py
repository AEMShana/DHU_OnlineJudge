from .models import ArticleColumn
from django.contrib import admin
from .models import ArticlePost

admin.site.register(ArticlePost)

# 注册文章栏目
admin.site.register(ArticleColumn)
