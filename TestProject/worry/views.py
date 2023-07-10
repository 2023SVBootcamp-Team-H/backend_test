from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from .models import Worry, Answer


from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Worry


@api_view(['GET'])
def get_worry(request, worry_id):
    try:
        worry = Worry.objects.get(id=worry_id)
        content = {
            'id': worry.id,
            'content': worry.content
        }
        return Response(content)
    except Worry.DoesNotExist:
        return Response(status=404)
