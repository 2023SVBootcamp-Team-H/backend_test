from django.db import models
from config.basemodel import BaseModel
from worry.models import Worry
from django_prometheus.models import ExportModelOperationsMixin


# Create your models here.


class Answer(ExportModelOperationsMixin('answer'), BaseModel):  # Answer 모델
    # Worry 모델과 1:1 관계
    worry = models.OneToOneField(Worry, on_delete=models.CASCADE)
    content = models.CharField(max_length=300)  # GPT가 답변한 내용
    likes = models.IntegerField(null=True)  # 좋아요 수

    def __str__(self):
        return self.content
