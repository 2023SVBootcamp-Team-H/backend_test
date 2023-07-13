from django.urls import path
from .views import *

urlpatterns = [
    path('', answer_get_score),
]
