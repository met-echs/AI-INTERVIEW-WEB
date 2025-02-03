# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('create_criteria/', views.manage_evaluation_criteria, name='manage_evaluation_criteria'),
    path('question_manage_criteria/', views.question_manage_criteria, name='question_manage_criteria'),
    path('question/<int:question_id>/', views.question_detail, name='question_detail'),
    path('high-scores/', views.high_scores, name='high_scores'),
    path('adminlogin/',views.login_page,name='admin_login')
]
