from django.db import models

# Create your models here.
class Personality(models.Model):
    name = models.CharField()
    frequency = models.IntegerField()
    popularity = models.IntegerField()
    total = models.FloatField()
    image_url = models.CharField()
    created_at = models.DateTimeField()
    modified_at = models.DateTimeField()
    


