from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from .models import Category

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
# Create your views here.

@api_view(['GET'])
def category(request):
    catagories = Category.objects.values()  # 쿼리셋(QuerySet)을 딕셔너리 형태로 반환
    return Response(catagories)

category_request_body_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "name": openapi.Schema(type=openapi.TYPE_STRING),
        "image_url": openapi.Schema(type=openapi.TYPE_STRING),
    }
)
@swagger_auto_schema(method='post', request_body=category_request_body_schema)
@api_view(['POST'])
def create_category(request):
    name = request.data.get('name')
    image_url = request.data.get('image_url')
    
    Category(name=name, image_url=image_url).save()
    
    return Response({'success': 'valid data'})