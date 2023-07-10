from django.db import models
from TestProject.basemodel import BaseModel
# Create your models here.


class Personality(BaseModel):
    name = models.CharField()
    frequency = models.IntegerField()
    popularity = models.IntegerField()
    total = models.FloatField()
    image_url = models.CharField()

    def __str__(self):
        return self.name
