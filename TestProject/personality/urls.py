from django.urls import path
from . import views

urlpatterns = [
    path('', views.personalities),
    path('score/', views.personalities_score),
    # path('create/', views.create_personality),
    # path('delete/', views.delete_personality),
]
