from django.urls import path
from . import views

app_name = 'team'

urlpatterns = [
    path('detail/<int:id>/', views.team_detail, name='detail'),

]