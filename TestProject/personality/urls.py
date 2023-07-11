from django.urls import path
from . import views

urlpatterns = [
    path('', views.personalities),
    path('score/', views.personalities_score),
    path('init/', views.init_personality),
]
