from django.urls import path, include
from django.contrib import admin
from rest_framework import routers
from .views import get_worry

router = routers.DefaultRouter()

urlpatterns = [
    path('', get_worry),
]
