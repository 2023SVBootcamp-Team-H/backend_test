from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from .models import Worry, Answer


from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Worry

# query string : /worry/?worry_id=1
# -> request.GET.get("worry_id") == 1

# path parameter : /worry/1/
# -> request["worry_id"] == 1


@api_view(['GET'])
def get_worry(request):
    id = request.GET.get("worry_id")
    try:
        worry = Worry.objects.get(id=id)
        content = f"{id}번째 고민 : {worry.content}"
        return Response(content)
    except Worry.DoesNotExist:
        return Response(status=404, data=f"{id}번째 고민이 없습니다.")
