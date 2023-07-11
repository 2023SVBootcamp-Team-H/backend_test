from django.db import models
from TestProject.basemodel import BaseModel
from user.models import User
from category.models import Category
from personality.models import Personality
from answer.models import Answer



class Worry(BaseModel):  # Worry 모델
    # TODO: 유저 모델을 연결해야함(FK)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # TODO: 카테고리 모델을 연결해야함(FK)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    # TODO: 인격 모델을 연결해야함(FK)
    personality = models.ForeignKey(Personality, on_delete=models.CASCADE)
    
    content = models.CharField(max_length=300)  # 내용
    
    # TODO: 답변 연결하기
    answer = models.CharField(max_length=300, null=True)
    # q.answer_set.all()로 접근 가능
    def __str__(self):
        return self.content
