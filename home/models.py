from django.db import models
from django.contrib.auth.models import User


class Testimonial(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    message = models.TextField(blank=False, null=False, max_length=3000)
    is_approved = models.BooleanField(default=False)
    is_awaiting_approval = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.user.first_name}\'s Testimonial'
