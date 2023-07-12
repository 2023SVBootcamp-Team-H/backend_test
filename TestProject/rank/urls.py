from django.urls import path
from .views import *

urlpatterns = [
    path('', rank),
    # path('gender', get_all_worry),
]
