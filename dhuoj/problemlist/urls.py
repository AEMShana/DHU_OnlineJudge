from django.urls import path
from . import views

app_name = 'problemlist'

urlpatterns = [
    path('detail/<int:id>/', views.problemlist_detail, name='detail'),
    path('create/<int:id>/', views.problemlist_create, name='create'),
]