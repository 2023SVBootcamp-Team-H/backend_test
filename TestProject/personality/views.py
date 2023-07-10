from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from .models import Personality

@api_view(['GET'])
def personalities(request):
    personalities = Personality.objects.values() #쿼리셋(QuerySet)을 딕셔너리 형태로 반환
    return Response(personalities)

@api_view(['POST'])
def personalities_score(request: Request):

    return Response({"content": f"{request.data}"})
