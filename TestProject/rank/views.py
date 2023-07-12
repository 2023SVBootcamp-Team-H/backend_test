from django.db.models import Avg
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from answer.models import *
from personality.models import *


@api_view(['GET'])
def rank(request: Request):
    result = []

    # 모든 인격 에서
    for p in Personality.objects.all():
        # worry__personality = p 로 외래키를 2번 건너 필터링 할수있다.
        objects_filter = Answer.objects.filter(worry__personality=p)
        # aggregate(avg=Avg('likes'))로 likes의 평균을 반환한다. (null이면 평균계산에 포함하지 않는다.)
        # { "avg" : 평균값 }
        avg = objects_filter.aggregate(avg=Avg('likes'))['avg']

        # 평균이 Null 이면 == 인격에 아무도 좋아요를 누르지 않았다면 0으로 치환!
        avg = avg if avg is not None else 0
        item = {
            "personality_name": p.name,
            "image_url": p.image_url,
            "avg": avg
        }
        result.append(item)
        # avg평균값을 기준으로 내림차순 정렬
    sorted_result = sorted(result, key=lambda x: x["avg"], reverse=True)
    return Response({"message": "success", "result": sorted_result})
