from django.db import models
from config.basemodel import BaseModel
from django_prometheus.models import ExportModelOperationsMixin

class Personality(ExportModelOperationsMixin('personality'),BaseModel):
    """
    GPT가 따라할 인격 모델
    
    속성:
        name: Char(50), 인격 이름
        image_url = Char(500), 인격 이미지 url
        content = Text, Prompt을 위한 초기 세팅 대화 
    """
    name = models.CharField(max_length=50, null=True)
    image_url = models.CharField(max_length=500, null=True)
    content = models.TextField(null=True)
    def __str__(self):
        return self.name
