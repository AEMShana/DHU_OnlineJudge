from django.shortcuts import render
from blog.models import ArticlePost
from problemset.models import Problem


def home(request):
    new_article = ArticlePost.objects.all()[:3]
    new_problem = Problem.objects.all()[:3]
    context = {
        "new_article": new_article,
        "new_problem": new_problem,
    }
    return render(request, 'home/index.html', context)
