from django.urls import path
from .views import *

urlpatterns = [
    path('<int:worry_id>', get_one_worry),
    path('', get_all_worry),
]
