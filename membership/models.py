from django.contrib.auth.models import User
from django.db import models
from datetime import timedelta
import datetime
from django.utils import timezone


class MembershipUpdateStatus(models.Model):
    friendly_name = models.CharField(max_length=254)
    name = models.CharField(max_length=254, unique=True, editable=False)
    last_updated_date = models.DateField(default=None, null=True, blank=True)

    def __str__(self):
        return f'{self.last_updated_date.strftime("%m-%d-%Y")}'


class MembershipPackage(models.Model):
    name = models.CharField(max_length=254, unique=True)
    friendly_name = models.CharField(max_length=254)
    description = models.TextField()
    duration = models.IntegerField(verbose_name='Duration (days)')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=27.00, verbose_name='Price ($USD)')
    checkout_url = models.URLField()

    def __str__(self):
        return f'{self.friendly_name}'

class MembershipStatus(models.Model):
    name = models.CharField(max_length=254, unique=True)
    friendly_name = models.CharField(max_length=254)
    description = models.TextField(max_length=3000, blank=True)
    valid = models.BooleanField(default=False, verbose_name='Validity')

    def __str__(self):
        return f'{self.friendly_name}'


class Membership(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    status = models.ForeignKey(MembershipStatus, on_delete=models.SET_NULL, null=True)
    status_name = models.CharField(max_length=254)
    is_valid = models.BooleanField(default=False, verbose_name='Validity')
    purchase_date = models.DateField(default=datetime.date.today, blank=True, null=True)  # Use a callable
    start_date = models.DateField(default=None, blank=True, null=True)
    end_date = models.DateField(default=None, blank=True, null=True)
    package = models.ForeignKey(MembershipPackage, on_delete=models.SET_NULL, null=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.user.first_name}\'s Membership'
    
    def save(self, *args, **kwargs):
        # Calculate cost based on package price
        if self.package:
            self.cost = self.package.price
            
        if self.status:
            self.is_valid = self.status.valid

            if self.status_name == 'pending':
                if self.status.name == 'active':
                    self.start_date = datetime.datetime.today()
                    self.end_date = self.start_date + timedelta(days=self.package.duration)
                    self.status_name = 'active'
                else:
                    self.purchase_date = datetime.datetime.today()
            elif self.status_name == 'active_renewal_pending':
                if self.status.name == 'active':
                    self.end_date = self.end_date + timedelta(days=self.package.duration)
                    self.status_name = 'active'
                else:
                    self.purchase_date = datetime.datetime.today()
            else:
                self.status_name = self.status.name

            if self.status.name == 'canceled':
                self.purchase_date = None
        
        super().save(*args, **kwargs)

    

