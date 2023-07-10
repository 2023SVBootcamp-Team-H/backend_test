from django.db import models
from TestProject.basemodel import BaseModel

# BaseModel -> Created_at, Modified_at, Deleted_at


class Worry(BaseModel):  # Worry 모델
    # TODO: 유저 모델을 연결해야함(FK)
    # TODO: 카테고리 모델을 연결해야함(FK)
    # TODO: 인격 모델을 연결해야함(FK)
    # TODO: 답변 모델을 연결해야함(FK)
    content = models.TextField()  # 내용

    def __str__(self):
        return self.content
