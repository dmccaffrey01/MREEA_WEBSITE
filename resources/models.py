from django.db import models
from datetime import datetime


class ResourceType(models.Model):
    name = models.CharField(max_length=254, blank=False, null=False)
    friendly_name = models.CharField(max_length=254, blank=False, null=False)
    icon_url = models.URLField(max_length=1024, null=True, blank=True)
    icon = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.friendly_name

class Folder(models.Model):
    name = models.CharField(max_length=254, blank=False, null=False)
    friendly_name = models.CharField(max_length=254, blank=False, null=False)
    icon_url = models.URLField(max_length=1024, null=True, blank=True)
    icon = models.ImageField(null=True, blank=True)
    date = models.DateField(null=True, blank=True, default=datetime.now)
    parent_folder = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subfolders')

    def __str__(self):
        return self.friendly_name

class Resource(models.Model):
    name = models.CharField(max_length=254, blank=False, null=False)
    friendly_name = models.CharField(max_length=254, blank=False, null=False)
    date = models.DateField(default=datetime.now)
    resource_type = models.ForeignKey(ResourceType, on_delete=models.CASCADE)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE)
    link = models.URLField(max_length=1024, null=True, blank=True)

    def __str__(self):
        return self.friendly_name