from django.db import models
from config.basemodel import BaseModel
from user.models import User
from category.models import Category
from personality.models import Personality
from django_prometheus.models import ExportModelOperationsMixin

class Worry(ExportModelOperationsMixin('worry'),BaseModel):  # Worry 모델
    
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,null=True)
    personality = models.ForeignKey(Personality, on_delete=models.CASCADE,null=True)
    
    content = models.CharField(max_length=300)  # 내용
    # q.answer_set.all()로 접근 가능
    def __str__(self):
        return self.content
