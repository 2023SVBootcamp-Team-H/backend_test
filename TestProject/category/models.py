from TestProject.basemodel import BaseModel
from django.db import models


class Category(BaseModel):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    image_url = models.CharField(max_length=500)

    def __str__(self):
        return self.name
