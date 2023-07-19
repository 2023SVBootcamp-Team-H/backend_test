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

personalities_get_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'personalities_id': openapi.Schema(type=openapi.TYPE_INTEGER),
        'created_at':openapi.Schema(type=openapi.FORMAT_DATETIME),
        'updated_at':openapi.Schema(type=openapi.FORMAT_DATETIME),
        'deleted_at':openapi.Schema(type=openapi.FORMAT_DATETIME, nullable=True),
        'name': openapi.Schema(type=openapi.TYPE_STRING),
        'image_url': openapi.Schema(type=openapi.TYPE_STRING),
    }
)

@swagger_auto_schema(
    method='get',
    operation_description="인격 전체 조회",
    responses={200: personalities_get_response_schema}
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
        Personality(name=name).save()

        return Response({"message": "Personality objects created successfully"})
    elif request.method == 'DELETE':
        p_list = Personality.objects.all()
        for i in p_list:
            i.delete()
        return Response({"message": "Personality objects all Delete"})
