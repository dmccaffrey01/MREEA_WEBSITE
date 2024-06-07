import string
import random
from django.db import models
from datetime import datetime
from django.utils import timezone


class Icon(models.Model):
    name = models.CharField(max_length=254, unique=True)
    friendly_name = models.CharField(max_length=254, blank=False, null=False)
    icon = models.TextField()

    def __str__(self):
        return self.friendly_name
    

class Folder(models.Model):
    name = models.CharField(max_length=254, unique=True)
    friendly_name = models.CharField(max_length=254, blank=False, null=False)
    parent_folder = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subfolders')
    icon = models.ForeignKey(Icon, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(default=timezone.now)
    is_deleted = models.BooleanField(default=False)

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
    name = models.CharField(max_length=254, unique=True)
    friendly_name = models.CharField(max_length=254, blank=True, null=True)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE)
    url = models.CharField(max_length=1024, blank=True, null=True)
    icon = models.ForeignKey(Icon, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

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
