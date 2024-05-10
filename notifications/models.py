from django.db import models
from django.contrib.auth.models import User
import string
import random


class Notification(models.Model):
    sku = models.CharField(max_length=254, unique=True, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    heading = models.CharField(max_length=254, null=True, blank=True)
    message = models.TextField(max_length=3000)
    date = models.DateTimeField(auto_now_add=True)
    cleared_status = models.BooleanField(default=False)
    category = models.CharField(max_length=254, null=True, blank=True)
    url = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.sku
    
    def save(self, *args, **kwargs):
        if not self.sku:  # If name is not provided
            self.sku = self.generate_unique_sku()
        super().save(*args, **kwargs)

    def generate_unique_sku(self):
        prefix = 'NOT'
        suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        return prefix + suffix