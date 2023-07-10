from django.urls import path,include
from django.contrib import admin
from rest_framework import routers

from worry.views import WorryViewSet, AnswerViewSet

router = routers.DefaultRouter()

router.register('worry', WorryViewSet)
router.register('answer', AnswerViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]