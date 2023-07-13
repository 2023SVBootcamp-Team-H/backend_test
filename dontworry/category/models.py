from config.basemodel import BaseModel
from django.db import models
from django_prometheus.models import ExportModelOperationsMixin

class Category(ExportModelOperationsMixin('category'),BaseModel):
    name = models.CharField(max_length=50)
    image_url = models.CharField(max_length=500)

    def __str__(self):
        return self.name
