from django.urls import path
from . import views

urlpatterns = [
    path('', views.category),
    path('create/', views.create_category),
]
