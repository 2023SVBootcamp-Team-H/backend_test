from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Worry

# query string : /worry/?worry_id=1
# -> request.GET.get("worry_id") == 1

# path parameter : /worry/1/
# -> request["worry_id"] == 1

# 모든 고민 조회


@api_view(['GET'])
def get_all_worry(request):
    worries = Worry.objects.all()
    content = []
    for worry in worries:
        content.append({
            'id': worry.id,
            'content': worry.content
        })
    return Response(content)

# 특정 id 고민 조회


@api_view(['GET'])
def get_one_worry(request):
    id = request.GET.get("worry_id")
    try:
        worry = Worry.objects.get(id=id)
        content = f"{id}번째 고민 : {worry.content}"
        return Response(content)
    except Worry.DoesNotExist:
        return Response(status=404, data=f"{id}번째 고민이 없습니다.")

# 고민 생성


@api_view(['POST'])
def post_worry(request):
    content = request.data['content']
    worry = Worry.objects.create(content=content)
    return Response(status=201, data=f"{worry.id}번째 고민이 생성되었습니다.")

# 고민 수정


@api_view(['PUT'])
def update_worry(request):
    id = request.data['id']
    content = request.data['content']
    try:
        worry = Worry.objects.get(id=id)
        worry.content = content
        worry.save()
        return Response(status=200, data=f"{id}번째 고민이 수정되었습니다.")
    except Worry.DoesNotExist:
        return Response(status=404, data=f"{id}번째 고민이 없습니다.")

# 고민 삭제


@api_view(['DELETE'])
def delete_worry(request):
    id = request.data['id']
    try:
        worry = Worry.objects.get(id=id)
        worry.delete()
        return Response(status=200, data=f"{id}번째 고민이 삭제되었습니다.")
    except Worry.DoesNotExist:
        return Response(status=404, data=f"{id}번째 고민이 없습니다.")
