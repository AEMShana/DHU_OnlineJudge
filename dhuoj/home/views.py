from django.shortcuts import render
from blog.models import ArticlePost, ArticleColumn
from problemset.models import Problem


def home(request):
    new_article = ArticlePost.objects.all()[:3]
    new_problem = Problem.objects.all()[:3]
    news = ArticlePost.objects.filter(column__title="新闻")[:3]
    print(news)
    context = {
        "new_article": new_article,
        "new_problem": new_problem,
        "news": news
    }
    return render(request, 'home/index.html', context)
