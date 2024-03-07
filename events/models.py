import string
import random
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from resources.models import Folder
from django.db.models.signals import pre_delete

class Event(models.Model):
    name = models.CharField(max_length=255, unique=True, editable=False)
    friendly_name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(max_length=3000, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    duration = models.IntegerField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    folder = models.ForeignKey(Folder, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.friendly_name
    
    def save(self, *args, **kwargs):
        if not self.name:  # If name is not provided
            self.name = self.generate_unique_name()
        super().save(*args, **kwargs)

    def generate_unique_name(self):
        prefix = 'E'
        suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        return prefix + suffix
    

@receiver(post_save, sender=Event)
def create_folder(sender, instance, created, **kwargs):
    if created and not instance.folder:
        parent_folder = Folder.objects.get(name="events")
        friendly_name = instance.friendly_name

        folder = Folder.objects.create(
            name="",
            friendly_name=friendly_name,
            parent_folder=parent_folder
        )
        folder.save()
        instance.folder = folder
        instance.save()


@receiver(pre_delete, sender=Event)
def delete_folder(sender, instance, **kwargs):
    if instance.folder:
        instance.folder.delete()