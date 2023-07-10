from django.db import models

class User(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    age = models.SmallIntegerField()
    sex = models.CharField(max_length=6, choices=[('male', 'Male'), ('female', 'Female')])
    job = models.CharField(max_length=50)
    nickname = models.CharField(max_length=50)
    address = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.TimeField()
    modified_at = models.TimeField(blank=True, null=True)
    deleted_at = models.TimeField(blank=True, null=True)

    def __str__(self):
        return self.nickname
