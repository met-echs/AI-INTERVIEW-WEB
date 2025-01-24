from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'), 
    path('interview/', views.index, name='index'),
    path('question/<int:question_id>/', views.get_question, name='get_question'),
    path('start_transcription/', views.start_transcription, name='start_transcription'),
    path('stop_transcription/', views.stop_transcription, name='stop_transcription'),
    path('live_transcribe/', views.live_transcribe, name='live_transcribe'),
]