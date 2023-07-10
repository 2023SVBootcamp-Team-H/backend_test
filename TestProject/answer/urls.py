from django.urls import path
from .views import *

urlpatterns = [
    path('', get_one_answer),
    path('all', get_all_answer),
    path('post', post_answer),
    path('update', update_answer),
    path('delete', delete_answer),
]
