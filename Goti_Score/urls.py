  
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('score/<int:pk>', views.score_card, name='score_card'),
    
]