from django.db import models
from config.basemodel import BaseModel
from worry.models import Worry
from django_prometheus.models import ExportModelOperationsMixin

class Answer(ExportModelOperationsMixin('answer'), BaseModel): 
    """
    답변 모델
    
    속성:
        worry: FK, Worry 모델과 1:1 관계
        content: Char(300),nullable, GPT가 답변한 내용
        likes: Integer, 좋아요 수
        
        
    """
    
    worry = models.OneToOneField(Worry, on_delete=models.CASCADE)
    content = models.CharField(max_length=300)
    likes = models.IntegerField(null=True)

    def __str__(self):
        return self.content
