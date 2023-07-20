from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Answer
from worry.models import Worry
answer_get_responses_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'answers_id':openapi.Schema(type=openapi.TYPE_INTEGER),
        'created_at':openapi.Schema(type=openapi.FORMAT_DATETIME),
        'updated_at':openapi.Schema(type=openapi.FORMAT_DATETIME),
        'worry_id':openapi.Schema(type=openapi.TYPE_INTEGER),
        'content':openapi.Schema(type=openapi.TYPE_STRING),
        'likes':openapi.Schema(type=openapi.TYPE_INTEGER),
    }
)
answer_post_body_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'answer_id': openapi.Schema(type=openapi.TYPE_INTEGER),
        'likes': openapi.Schema(type=openapi.TYPE_INTEGER),
        # 필요한 필드들을 추가로 정의합니다.
    }
)
answer_responses_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'message': openapi.Schema(type=openapi.TYPE_STRING),
    }
)
response_schema_4XX = openapi.Schema(
    type=openapi.TYPE_STRING,
    description="4xx 에러입니다."
)
@swagger_auto_schema(
    method='get',
    operation_description="답변 전체 조회",
    responses={200: answer_get_responses_schema}
)
@swagger_auto_schema(
    method='post',
    request_body=answer_post_body_schema,
    responses={200: answer_responses_schema,
               404: response_schema_4XX},
    operation_description="put.body.answer_id, put.body.likes를 이용해 인기 등록",
)
@swagger_auto_schema(
    method='delete',
    operation_description="delete.body.answer_id 에 해당하는 answer삭제",
)
@api_view(['GET', 'POST', 'DELETE'])
def answer_get_score(request):
    """
        GET : 답변 전체 조회
        
        POST : 답변 인기도 투표
        
        DELETE : 답변 삭제
    """
    
    # 전체 답변 조회
    if request.method == 'GET':
        answers = Answer.objects.values()
        return Response(status=200, data=answers)

    # 해당 답변에 인기도 투표하기
    elif request.method == 'POST':
        if 'likes' not in request.data:
            return Response(status=404, data=f"like 속성이 없습니다.")
        if 'answer_id' not in request.data:
            return Response(status=404, data=f"answer_id 속성이 없습니다.")

        answer_id = request.data['answer_id']
        answer_likes = request.data['likes']
        try:
            answer = Answer.objects.get(id=answer_id)
            answer.likes = answer_likes
            answer.save()
            return Response(status=200, data=f"{answer_id}번째 답변이 {answer_likes}으로 설정되었습니다.")
        except Answer.DoesNotExist:
            return Response(status=404, data=f"{answer_id}번째 답변이 없습니다.")

    # 특정 답변 삭제
    elif request.method == 'DELETE':
        try :
            answer_id = request.data["answer_id"]
            Answer.objects.get(answer_id=answer_id).delete()
        except Exception as e:
            return Response(status=404, data=f"{answer_id}답변이 없습니다.")
        return Response(status=200, data=f"{answer_id}답변이 삭제되었습니다.")
