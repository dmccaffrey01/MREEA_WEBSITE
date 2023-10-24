from django.db import models


class Event(models.Model):
    name = models.CharField(max_length=255, default="")
    description = models.TextField(max_length=255, blank=True, null=True)
    date = models.DateField()
    time = models.TimeField()
    duration = models.IntegerField()
    location = models.CharField(max_length=255, default="")
    
