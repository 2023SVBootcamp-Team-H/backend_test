from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from .models import Category

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


category_request_body_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "name": openapi.Schema(type=openapi.TYPE_STRING),
        "image_url": openapi.Schema(type=openapi.TYPE_STRING),
    }
)
category_get_responses_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "category_id": openapi.Schema(type=openapi.TYPE_INTEGER),    
        "name": openapi.Schema(type=openapi.TYPE_STRING),
        "image_url": openapi.Schema(type=openapi.TYPE_STRING),
    }
)

@swagger_auto_schema(
    method='get',
    responses={200: category_get_responses_schema},
    operation_description="모든 카테고리 조회")
@swagger_auto_schema(
    method='post',
    request_body=category_request_body_schema,
    responses={200: openapi.Response(description='Success')},           
    operation_description= "카테고리의 이름,카테고리의 이미지 url을 이용해 카테고리 생성"
)

@api_view(['GET', 'POST'])
def category(request : Request):
    if request.method == 'GET':
        catagories = Category.objects.values()  # 쿼리셋(QuerySet)을 딕셔너리 형태로 반환
        return Response(catagories)
    elif request.method == 'POST':
        name = request.data.get('name')
        image_url = request.data.get('image_url')

        Category.objects.create(name=name, image_url=image_url)

        return Response({'success': 'valid data'})
    
@swagger_auto_schema(
method='post',
responses={200: openapi.Response(description='Success')},           
operation_description= "카테고리별 이름 저장"
)

@api_view(['POST'])
def set_category(request):
    if request.method == 'POST':
        Category.objects.all().delete()
        # list_category = len(Category.objects.all())
        
        # for i in range(list_category):
        #     Category.objects.filter().first().delete()

        c1=Category(name="학업",image_url="image_url").save()
        c2=Category(name="건강", image_url="image_url").save()
        c3=Category(name="경제", image_url="image_url").save()
        c4=Category(name="가족관계", image_url="image_url").save()
        c5=Category(name="결혼", image_url="image_url").save()
        c6=Category(name="미래", image_url="image_url").save()
        c7=Category(name="취미", image_url="image_url").save()
        c8=Category(name="우정", image_url="image_url").save()
        c9=Category(name="직장/알바", image_url="image_url").save()
        c10=Category(name="진로/취업", image_url="image_url").save()
        c11=Category(name="군대", image_url="image_url").save()
        c12=Category(name="연애", image_url="image_url").save()
        c13=Category(name="운동", image_url="image_url").save()
        c14=Category(name="육아", image_url="image_url").save()

        return Response({'success': 'valid data'})
