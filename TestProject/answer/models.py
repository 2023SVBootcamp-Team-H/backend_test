from django.db import models
from TestProject.basemodel import BaseModel
from worry.models import Worry
# Create your models here.


class Answer(BaseModel):  # Answer 모델
    worry = models.ForeignKey(
        Worry, on_delete=models.CASCADE)  # Worry 모델과 1:1 관계
    content = models.CharField(max_length=300)  # GPT가 답변한 내용

    def __str__(self):
        return self.content
