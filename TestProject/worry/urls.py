from django.urls import path, include
from django.contrib import admin
from rest_framework import routers
from .views import get_worry

router = routers.DefaultRouter()

urlpatterns = [
    path('<int:worry_id>', get_worry),
]
