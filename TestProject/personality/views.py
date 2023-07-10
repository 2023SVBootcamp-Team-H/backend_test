from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from .models import Personality
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

@api_view(['GET'])
def personalities(request):
    personalities = Personality.objects.values() #쿼리셋(QuerySet)을 딕셔너리 형태로 반환
    return Response(personalities)

score_request_body_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'personality_name': openapi.Schema(type=openapi.TYPE_STRING),
        'score': openapi.Schema(type=openapi.TYPE_INTEGER),
        # 필요한 필드들을 추가로 정의합니다.
    }
)
score_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'message': openapi.Schema(type=openapi.TYPE_STRING),
        # 필요한 필드들을 추가로 정의합니다.
    }
)


@swagger_auto_schema(method='post', request_body=score_request_body_schema, responses={200: score_response_schema})
@api_view(['POST'])
def personalities_score(request: Request):
    res = {"message": "success"}
    body = request.data
    # 만약 요청 값이 없다면 fail return
    if "personality_name" not in body or "score" not in body:
        res = {"message": "바디값을 확인하세요"}
        return Response(res)

    # 바디값 가져오기
    personality_name = body.get("personality_name")
    score = body.get("score")

    # 인격 점수를 올리는 로직
    try:
        personality = Personality.objects.get(name=personality_name)
        personality.total += score
        personality.save()
    except Personality.DoesNotExist:
        return Response({"message": "해당하는 인격 이름이 없습니다."})

    return Response({"message": f"{personality_name}인격의 인기도가 {score}만큼 올라갔습니다."})
