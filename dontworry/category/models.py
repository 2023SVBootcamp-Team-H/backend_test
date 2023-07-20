from config.basemodel import BaseModel
from django.db import models
from django_prometheus.models import ExportModelOperationsMixin

class Category(ExportModelOperationsMixin('category'),BaseModel):
    """
        고민의 카테고리를 나타내는 모델

        속성:
            name: Char(50), 카테고리 이름
            image_url = Char(500), 카테고리 이미지 url
    """
    name = models.CharField(max_length=50)
    image_url = models.CharField(max_length=500)

    def __str__(self):
        return self.name
