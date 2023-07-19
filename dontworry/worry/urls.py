from django.urls import path
from .views import *

urlpatterns = [
    path('<int:worry_id>', get_one_worry),
    path('test/<int:page>', get_best_worry_answer),
    path('', get_all_worry),
    path('sse', sse_request),
]
