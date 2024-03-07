import string
import random
from django.db import models
from datetime import datetime


class ResourceType(models.Model):
    name = models.CharField(max_length=254, blank=False, null=False)
    friendly_name = models.CharField(max_length=254, blank=False, null=False)
    icon_url = models.URLField(max_length=1024, null=True, blank=True)
    icon = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.friendly_name
    
    def save(self, *args, **kwargs):
        if not self.name:  # If name is not provided
            self.name = self.generate_unique_name()
        super().save(*args, **kwargs)

    def generate_unique_name(self):
        prefix = 'RT'
        suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        return prefix + suffix


class Folder(models.Model):
    name = models.CharField(max_length=254, unique=True)
    friendly_name = models.CharField(max_length=254, blank=False, null=False)
    icon_url = models.URLField(max_length=1024, null=True, blank=True)
    icon = models.ImageField(null=True, blank=True)
    date = models.DateField(null=True, blank=True, default=datetime.now)
    parent_folder = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subfolders')
    quick_resources = models.BooleanField(default=False)

    def __str__(self):
        return self.friendly_name
    
    def save(self, *args, **kwargs):
        if not self.name:  # If name is not provided
            self.name = self.generate_unique_name()
        super().save(*args, **kwargs)

    def generate_unique_name(self):
        prefix = 'F'
        suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        return prefix + suffix

class Resource(models.Model):
    name = models.CharField(max_length=254, blank=False, null=False)
    friendly_name = models.CharField(max_length=254, blank=False, null=False)
    date = models.DateField(default=datetime.now)
    resource_type = models.ForeignKey(ResourceType, on_delete=models.CASCADE)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE)
    link = models.URLField(max_length=1024, null=True, blank=True)

    def __str__(self):
        return self.friendly_name
    
    def save(self, *args, **kwargs):
        if not self.name:  # If name is not provided
            self.name = self.generate_unique_name()
        super().save(*args, **kwargs)

    def generate_unique_name(self):
        prefix = 'R'
        suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        return prefix + suffix
