from django.db import models
from config.basemodel import BaseModel
from django_prometheus.models import ExportModelOperationsMixin

class User(ExportModelOperationsMixin('user'),BaseModel):
    """
    User 모델
    속성: 
        age: SmallInteger, 나이
        gender: Char(6), 성별
        job: Char(50), 직업
        nickname: Char(50), 닉네임
        address: Char(50), 주소
    """
    age = models.SmallIntegerField()
    gender = models.CharField(max_length=6, choices=[('male', 'Male'), ('female', 'Female')])
    job = models.CharField(max_length=50)
    nickname = models.CharField(max_length=50)
    address = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.nickname
