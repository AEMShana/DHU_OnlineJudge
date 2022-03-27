from django.urls import path
from . import views

app_name = 'comment'

urlpatterns = [
    # 一级评论
    path('post-comment/<int:article_id>/', views.post_comment, name='post_comment'),
    # 二级评论
    path('post-comment/<int:article_id>/<int:parent_comment_id>', views.post_comment, name='comment-reply'),
]