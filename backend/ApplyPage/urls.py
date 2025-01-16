from django.urls import path
from . import views

urlpatterns = [
    path('', views.home,name="index"),
    path('', views.upload_resume,name="index"),
    
]
