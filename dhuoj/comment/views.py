from hashlib import new
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import markdown

from blog.models import ArticlePost
from .forms import CommentForm
from .models import Comment

# 文章评论
@login_required(login_url='/userprofile/login/')
def post_comment(request, article_id, parent_comment_id=None):
    article = get_object_or_404(ArticlePost, id=article_id)

    # 处理 POST 请求
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.body = markdown.markdown(new_comment.body,
                                                extensions=[
                                                    'markdown.extensions.extra',
                                                    'markdown.extensions.codehilite',
                                                    'pymdownx.arithmatex',
                                                ]
            )
            new_comment.article = article
            new_comment.user = request.user
            # 二级回复
            if parent_comment_id:
                parent_comment = Comment.object.get(id=parent_comment_id)
                new_comment.parent_id = parent_comment.get_root().id
                new_comment.reply_to = parent_comment.user
                new_comment.save()
                return HttpResponse('200 OK')
            new_comment.save()
            return redirect("blog:article_detail", id=article_id)
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    elif request.method == 'GET':
        comment_form = CommentForm()
        context = {
            'commnet_form': comment_form,
            'article_id': article_id,
            'parent_comment_id': parent_comment_id
        }
        return render(request, 'comment/reply.html', context)
    # 处理错误请求
    else:
        return HttpResponse("发表评论仅接受POST请求。")