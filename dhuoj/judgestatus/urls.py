from django.urls import path
from . import views
app_name = 'judgestatus'

urlpatterns = [
    path('<user_name>', views.status_list, name='status_list'),

]
