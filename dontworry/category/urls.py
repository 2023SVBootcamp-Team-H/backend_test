from django.urls import path
from . import views

urlpatterns = [
    path('', views.category),
    path('setc/', views.set_category),
]
