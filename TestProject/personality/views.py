from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from .models import Personality


@api_view(['GET'])
def personalities(request):
    personalities = Personality.objects.all()
    # content = [
    #     'id': personality.id,
    #     'name': personality
    # ]
    return Response()


@api_view(['POST'])
def personalities_score(request: Request):

    return Response({"content": f"{request.data}"})
