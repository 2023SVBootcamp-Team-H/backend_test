from django.urls import path
from . import views

urlpatterns = [
    path('', views.personalities),
    path('set/', views.set_personalities),
]
