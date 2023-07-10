from django.urls import path
from .views import *

urlpatterns = [
    path('', get_one_worry),
    path('all', get_all_worry),
    path('post', post_worry),
    path('update', update_worry),
    path('delete', delete_worry),

]
