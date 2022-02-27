from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import ArticlePost
import markdown


def article_list(request):
    articles = ArticlePost.objects.all()
    context = {'articles': articles}
    return render(request, 'blog/list.html', context)


def article_detail(request, id):
    article = ArticlePost.objects.get(id=id)
    article.body = markdown.markdown(article.body,
                                     extensions=[
                                         'markdown.extensions.extra',
                                         'markdown.extensions.codehilite',
                                         'pymdownx.arithmatex',
                                     ]
                                     )
    context = {'article': article}
    return render(request, 'blog/detail.html', context)
