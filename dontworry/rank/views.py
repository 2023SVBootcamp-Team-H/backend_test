from django.db.models import Avg
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from answer.models import *
from personality.models import *
from user.models import *


@swagger_auto_schema(
    method='get',
    operation_description="인격별 인기도 순위 조회"
)
@api_view(['GET'])
def rank(request: Request):
    result = []

    # 모든 인격 에서
    for p in Personality.objects.all():
        # worry__personality = p 로 외래키를 2번 건너 필터링 할수있다.정
        objects_filter = Answer.objects.filter(worry__personality=p)
        # aggregate(avg=Avg('likes'))로 likes의 평균을 반환한다. (null이면 평균계산에 포함하지 않는다.)
        # { "avg" : 평균값 }
        avg = objects_filter.aggregate(avg=Avg('likes'))['avg']

        # 평균이 Null 이면 == 인격에 아무도 좋아요를 누르지 않았다면 -1으로 치환!
        avg = avg if avg is not None else -1
        item = {
            "personality_name": p.name,
            "image_url": p.image_url,
            "avg": avg
        }
        result.append(item)
        # avg평균값을 기준으로 내림차순 정렬
    sorted_result = sorted(result, key=lambda x: x["avg"], reverse=True)
    return Response({"message": "success", "result": sorted_result})

@swagger_auto_schema(
    method='get',
    operation_description="인격, 성별 별 인기도 순위 조회"
)
@api_view(['GET'])
def gender(request: Request):
    result = {}

    # distinct메소드를 이용해 성별 리스트를 얻는다 => [{ "gender":"male"},{"gender":"female"}]
    gender_list = User.objects.values('gender').distinct()
    # map 을 이용해 list 안 요소 변경 => ["male","female"]
    gender_list = list(map(lambda x: x["gender"], gender_list))
    for gender in gender_list:
        temp = []
        # 모든 인격 에서
        for p in Personality.objects.all():
            # 인격조건과 성별 조건이 맞는 답변 목록
            objects_filter = Answer.objects.filter(worry__user__gender=gender, worry__personality=p)
            avg = objects_filter.aggregate(avg=Avg('likes'))['avg']
            # 아무 투표가 없으면 -1로 표기
            avg = avg if avg is not None else -1
            item = {
                "personality_name": p.name,
                "image_url": p.image_url,
                "avg": avg
            }
            temp.append(item)
        # avg평균값을 기준으로 내림차순 정렬
        sorted_temp = sorted(temp, key=lambda x: x["avg"], reverse=True)
        result[gender] = sorted_temp
    return Response({"message": "success", "result": result})
