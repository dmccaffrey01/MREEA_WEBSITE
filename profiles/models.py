import uuid
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class Class(models.Model):
    name = models.CharField(max_length=254, unique=True)
    friendly_name = models.CharField(max_length=254)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name

class Category(models.Model):
    name = models.CharField(max_length=254, unique=True)
    friendly_name = models.CharField(max_length=254)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    first_name = models.CharField(max_length=254, blank=False)
    last_name = models.CharField(max_length=254, blank=False)
    full_name = models.CharField(max_length=254, blank=False)
    title = models.CharField(max_length=254, blank=True)
    bio = models.TextField(max_length=3000, blank=True)
    facebook_link = models.URLField(max_length=254, blank=True)
    email = models.EmailField(max_length=254, blank=True)
    phone_number = models.CharField(max_length=254, blank=True)
    class_field = models.ForeignKey('Class', null=True, blank=True, on_delete=models.SET_NULL)
    category_field = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)
    
    def __str__(self):
        return f'{self.first_name}\'s Profile'

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def save(self, *args, **kwargs):
        if not self.first_name and self.user.first_name:
            self.first_name = self.user.first_name
        if not self.last_name and self.user.last_name:
            self.last_name = self.user.last_name
        if self.first_name and self.last_name:
            self.full_name = self.get_full_name()

        if not self.pk:
            class_field = Class.objects.get(name="none")
            category_field = Category.objects.get(name="none")

            self.class_field = class_field
            self.category_field = category_field
        super().save(*args, **kwargs)


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Create or update the user profile
    """
    if created:
        # Generate a random username using UUID
        instance.username = uuid.uuid4().hex[:30]  # Limit to 30 characters
        instance.save()
    
    # Check if UserProfile exists for the user
    profile, _ = UserProfile.objects.get_or_create(user=instance)
    
    # Update the profile fields if necessary
    if not profile.first_name and instance.first_name:
        profile.first_name = instance.first_name
    if not profile.last_name and instance.last_name:
        profile.last_name = instance.last_name
    if profile.first_name and profile.last_name:
        profile.full_name = f'{profile.first_name} {profile.last_name}'
    profile.save()