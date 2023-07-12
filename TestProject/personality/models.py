from django.db import models
from TestProject.basemodel import BaseModel
from django_prometheus.models import ExportModelOperationsMixin

class Personality(ExportModelOperationsMixin('personality'),BaseModel):
    name = models.CharField(max_length=50, null=True)
    image_url = models.CharField(max_length=500, null=True)

    def __str__(self):
        return self.name
