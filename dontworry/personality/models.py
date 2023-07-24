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

    
class Static_Personality(models.Model):
    personality = models.OneToOneField(Personality, on_delete=models.CASCADE)
    temperature= models.FloatField(null=True)
    max_tokens= models.IntegerField(null=True)
    top_p= models.FloatField(null=True)
    frequency_penalty= models.FloatField(null=True)
    presence_penalty= models.FloatField(null=True)
    stop= models.CharField(max_length=50, null=True)
    prompt = models.CharField(max_length=200, null=True)
    def __str__(self):
        return self.personality.name+'static'
    