from django.contrib.auth.models import User
from django.db import models
from datetime import timedelta


class Membership(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_valid = models.BooleanField(default=False)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()

    def __str__(self):
        return f'{self.user.email}\'s Membership'
    
    def save(self, *args, **kwargs):
        # Set the end date to be one year from the start date
        if not self.pk:  # Check if the object is being created for the first time
            self.end_date = self.start_date + timedelta(days=365)
        super().save(*args, **kwargs)

    

