from django.db import models


class Personality(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50, null=True)
    frequency = models.IntegerField()
    popularity = models.IntegerField()
    total = models.FloatField()
    image_url = models.CharField(max_length=500, null=True)
    created_at = models.DateTimeField(null=True)
    modified_at = models.DateTimeField(null=True)

    def __str__(self):
        return self.name
