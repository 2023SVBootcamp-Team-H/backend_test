from rest_framework import viewsets
from .models import Worry, Answer
from .serializer import WorrySerializer, AnswerSerializer

# Create your views here.

class WorryViewSet(viewsets.ModelViewSet):
    queryset = Worry.objects.all()
    serializer_class = WorrySerializer
    
class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer