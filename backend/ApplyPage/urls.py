from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_resume,name="apply"),
    path('thankyou/',views.thanku_page,name="thankyouapply"),
    
]
