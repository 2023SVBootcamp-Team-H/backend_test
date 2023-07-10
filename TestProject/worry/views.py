from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Worry, Answer
from .serializer import WorrySerializer, AnswerSerializer


@api_view(['GET'])
def get_worry(request):
    worries = Worry.objects.all()
    serializer = WorrySerializer(worries, many=True)
    return Response(serializer.data)
