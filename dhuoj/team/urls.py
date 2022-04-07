from django.urls import path
from . import views

app_name = 'team'

urlpatterns = [
    path('detail/<int:id>/', views.team_detail, name='detail'),
    path('', views.team_list, name='team_list'),
    path('team-create/', views.team_create, name='team_create'),
]
