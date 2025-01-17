# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('create_criteria/', views.manage_evaluation_criteria, name='manage_evaluation_criteria'),
    # path('delete-criteria/<int:criteria_id>/', views.delete_evaluation_criteria, name='delete_criteria'),
]
