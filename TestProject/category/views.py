from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from .models import Category

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Create your views here.
category_request_body_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "name": openapi.Schema(type=openapi.TYPE_STRING),
        "image_url": openapi.Schema(type=openapi.TYPE_STRING),
    }
)

@swagger_auto_schema(
    method='get',
    operation_description="모든 카테고리 조회")
@swagger_auto_schema(
    method='post',
    request_body=category_request_body_schema,
    operation_description="post.body.name, post.body.image_url 을 이용해 카테고리 생성")
@api_view(['GET', 'POST'])
def category(request : Request):
    if request.method == 'GET':
        catagories = Category.objects.values()  # 쿼리셋(QuerySet)을 딕셔너리 형태로 반환
        return Response(catagories)
    elif request.method == 'POST':
        name = request.data.get('name')
        image_url = request.data.get('image_url')

        Category(name=name, image_url=image_url).save()

        return Response({'success': 'valid data'})



@api_view(['POST'])
def create_category(request):
    name = request.data.get('name')
    image_url = request.data.get('image_url')

    Category(name=name, image_url=image_url).save()

    return Response({'success': 'valid data'})
