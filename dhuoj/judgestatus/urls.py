from django.urls import path
from . import views
app_name = 'judgestatus'

urlpatterns = [
    path('', views.status_list_all, name='status_list_all'),
    path('<user_name>', views.status_list, name='status_list'),

]
