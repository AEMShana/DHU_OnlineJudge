from cmath import log
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ArticlePostForm
from .models import ArticlePost
from django.contrib.auth.models import User
import markdown
from .models import ArticleColumn
from django.db.models import Q
from comment.models import Comment
from comment.forms import CommentForm


def article_list(request):
    search = request.GET.get('search')
    if search:
        articles = ArticlePost.objects.filter(
            Q(title__icontains=search) |
            Q(body__icontains=search) |
            Q(column__title__icontains=search)
        )
    else:
        search = ''
        articles = ArticlePost.objects.all()
    context = {'articles': articles, 'search': search}
    return render(request, 'blog/list.html', context)

def article_search(request, id):
    articles = ArticlePost.objects.filter(
        Q(title__icontains=id) |
        Q(body__icontains=id) |
        Q(column__title__icontains=id)
    )
    context = { 'articles': articles, 'search': id }
    return render(request, 'blog/list.html', context)


def article_detail(request, id):
    article = ArticlePost.objects.get(id=id)
    # 取出文章评论
    comments = Comment.objects.filter(article=id)
    article.total_views += 1
    article.save(update_fields=['total_views'])
    article.body = markdown.markdown(article.body,
                                     extensions=[
                                         'markdown.extensions.extra',
                                         'markdown.extensions.codehilite',
                                         'pymdownx.arithmatex',
                                     ]
                                     )
    comment_form = CommentForm()
    context = {'article': article,
               'comments': comments,
               'comment_form': comment_form,
               }
    return render(request, 'blog/detail.html', context)

# 写文章的视图


@login_required(login_url='/userprofile/login/')
def article_create(request):
    if request.method == "POST":
        article_post_form = ArticlePostForm(data=request.POST)
        if article_post_form.is_valid():
            new_article = article_post_form.save(commit=False)
            new_article.author = User.objects.get(id=request.user.id)
            if request.POST['column'] != 'none':
                new_article.column = ArticleColumn.objects.get(
                    id=request.POST['column'])
            new_article.save()
            return redirect("blog:article_list")
        else:
            return HttpResponse("input invalid !")
    else:
        article_post_form = ArticlePostForm()
        columns = ArticleColumn.objects.all()
        context = {'article_post_form': article_post_form, 'columns': columns}
        return render(request, 'blog/create.html', context)


@login_required(login_url='/userprofile/login/')
def article_safe_delete(request, id):
    if request.method == 'POST':
        article = ArticlePost.objects.get(id=id)
        if request.user != article.author:
            return HttpResponse("抱歉，你无权删除这篇文章。")
        article.delete()
        return redirect("blog:article_list")
    else:
        return HttpResponse("仅接受POST请求。")

# 更新文章的视图


@login_required(login_url='/userprofile/login/')
def article_update(request, id):
    # 获取需要修改的具体文章对象
    article = ArticlePost.objects.get(id=id)
    if request.user != article.author:
        return HttpResponse("抱歉，你无权修改这篇文章。")
    # 判断用户是否为 POST 提交表单数据
    if request.method == "POST":
        # 将提交的数据赋值到表单实例
        article_post_form = ArticlePostForm(data=request.POST)
        # 判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            # 保存新写入的 title、body 数据并保存
            article.title = request.POST['title']
            article.body = request.POST['body']
            if request.POST['column'] != 'none':
                article.column = ArticleColumn.objects.get(
                    id=request.POST['column'])
            else:
                article.column = None
            article.save()
            # 完成后返回到修改后的文章中。需传入文章 id
            return redirect("blog:article_detail", id=id)
        # 如果数据不合法，返回错误信息
        else:
            return HttpResponse("表单内容有误，请重新填写。")

    # 如果用户 GET 请求获取数据
    else:
        # 创建表单类实例
        article_post_form = ArticlePostForm()
        columns = ArticleColumn.objects.all()
        # 赋值上下文，将 article 文章对象也传递进去，以便提取旧的内容
        context = {'article': article,
                   'article_post_form': article_post_form, 'columns': columns, }
        # 将响应返回到模板
        return render(request, 'blog/update.html', context)
