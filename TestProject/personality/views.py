from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from .models import Personality
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

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

init_request_body_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'personality_name': openapi.Schema(type=openapi.TYPE_STRING),
    }
)
init_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'message': openapi.Schema(type=openapi.TYPE_STRING),
    }
)


@swagger_auto_schema(
    method='get',
    operation_description="인격 전체 조회",
)
@swagger_auto_schema(
    method='post',
    request_body=init_request_body_schema,
    responses={200: init_response_schema},
    operation_description="post.body.personality_name에 해당하는 인격 생성"
)
@swagger_auto_schema(
    method='delete',
    operation_description="인격 모두 삭제"
)
@api_view(['GET', 'POST', 'DELETE'])
def personalities(request: Request):
    if request.method == 'GET':
        personalities = Personality.objects.values()  # 쿼리셋(QuerySet)을 딕셔너리 형태로 반환
        return Response(personalities)
    elif request.method == 'POST':
        try:
            name = request.data.get("personality_name")
        except Exception as e:
            return Response({"message": "no attribute personality_name"})
        Personality(name=name, frequency=0, popularity=0, total=0).save()

        return Response({"message": "Personality objects created successfully"})
    elif request.method == 'DELETE':
        p_list = Personality.objects.all()
        for i in p_list:
            i.delete()
        return Response({"message": "Personality objects all Delete"})


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
        # 인격의 populate가 증가
        personality.popularity += score
        if personality.frequency != 0:
            # 빈번도가 0이 아니라면 total 증가
            personality.total = personality.popularity / personality.frequency
        else:
            return Response({"message": "빈번도가 0입니다."})

        personality.save()
    except Personality.DoesNotExist:
        return Response({"message": "해당하는 인격 이름이 없습니다."})

    return Response({"message": f"{personality_name}인격의 인기도가 {score}만큼 올라갔습니다."})


@swagger_auto_schema(method='post', request_body=init_request_body_schema, responses={200: init_response_schema})
@api_view(['POST'])
def create_personality(request: Request):
    try:
        name = request.data.get("personality_name")
    except Exception as e:
        return Response({"message": "no attribute personality_name"})
    Personality(name=name, frequency=0, popularity=0, total=0).save()

    return Response({"message": "Personality objects created successfully"})


@api_view(['DELETE'])
def delete_personality(request: Request):
    p_list = Personality.objects.all()
    for i in p_list:
        i.delete()
    return Response({"message": "Personality objects all Delete"})
