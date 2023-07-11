from django.db import models
from TestProject.basemodel import BaseModel

class Personality(BaseModel):
    name = models.CharField(max_length=50, null=True)
    frequency = models.IntegerField()
    popularity = models.IntegerField()
    total = models.FloatField()
    image_url = models.CharField(max_length=500, null=True)

    def __str__(self):
        return self.name
