from django.urls import path
from .views import *

urlpatterns = [
    path('<int:worry_id>', get_one_worry),
    path('test/<int:page>', get_best_worry_answer),
    path('', get_all_worry),
    
    # SSE 방식으로 실시간으로 데이터를 받아올 수 있음
    path('sse', sse_request),
]
