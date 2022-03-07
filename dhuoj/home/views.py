from django.shortcuts import render
from blog.models import ArticlePost


def home(request):
    new_article = ArticlePost.objects.all()[:3]
    context = {"new_article": new_article}
    return render(request, 'home/index.html', context)
