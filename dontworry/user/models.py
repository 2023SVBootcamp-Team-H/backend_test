from django.db import models
from config.basemodel import BaseModel
from django_prometheus.models import ExportModelOperationsMixin

class User(ExportModelOperationsMixin('user'),BaseModel):
    age = models.SmallIntegerField()
    gender = models.CharField(max_length=6, choices=[
                           ('male', 'Male'), ('female', 'Female')])
    job = models.CharField(max_length=50)
    nickname = models.CharField(max_length=50)
    address = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.nickname
