from django.urls import path
from . import views

app_name = 'problemset'

urlpatterns = [
    path('problem/<problem_id>', views.problem, name='problem'),
]
