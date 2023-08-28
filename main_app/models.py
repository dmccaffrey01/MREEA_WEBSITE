from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.db import models
from django.utils import timezone
import uuid
from cloudinary.models import CloudinaryField


class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("You must provide an email address")
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)
    
    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)
        


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=255, blank=True, default='')
    last_name = models.CharField(max_length=255, blank=True, default='')
    email = models.EmailField(blank=True, default='', unique=True)
    phone_number = models.CharField(max_length=255, blank=True, default='')

    member_uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    member_short_uuid = models.CharField(max_length=10, unique=True, editable=False, default='')

    def save(self, *args, **kwargs):
        if not self.member_short_uuid:
            self.member_short_uuid = str(self.member_uuid)[:10]
        super().save(*args, **kwargs)

    is_active = models.BooleanField(default="True")
    is_superuser = models.BooleanField(default="False")
    is_staff = models.BooleanField(default="False")
    is_member = models.BooleanField(default="False")

    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name
    
    def get_short_name(self):
        return self.first_name
    

class MemberProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, blank=True, default='')
    last_name = models.CharField(max_length=255, blank=True, default='')
    profile_image = CloudinaryField('Profile Image', null=True, blank=True, default='https://res.cloudinary.com/dikcjjfpo/image/upload/v1692718355/default-profile-pic_nwq7pg.png')
    profile_image_change = models.CharField(max_length=1000, blank=True, default='')
    display_email = models.BooleanField(default=True)
    email = models.EmailField(blank=True)
    display_number = models.BooleanField(default=True)
    phone_number = models.CharField(max_length=255, blank=True)
    website = models.CharField(max_length=255, blank=True, default='')
    facebook = models.CharField(max_length=255, blank=True, default='')

    bio = models.TextField(default='', blank=True)

    TEACHING_CATEGORY_CHOICES = (
        ('option1', 'option1'),
        ('option2', 'option2'),
        ('option3', 'option3'),
        ('nothing', 'nothing'),
    )
    teaching_category = models.CharField(max_length=50, choices=TEACHING_CATEGORY_CHOICES, default='nothing')

    CLASSES_CHOICES = (
        ('option1', 'option1'),
        ('option2', 'option2'),
        ('option3', 'option3'),
        ('nothing', 'nothing'),
    )
    classes = models.CharField(max_length=50, choices=CLASSES_CHOICES, default='nothing')

    is_member = models.BooleanField(default='False')

    def save(self, *args, **kwargs):
        if self.user.is_superuser and not self.user.first_name:
            self.user.first_name = "Admin"
            self.user.save()
        if not self.pk:  # Only set default values for new instances
            self.first_name = self.user.first_name
            self.last_name = self.user.last_name
            self.email = self.user.email
            self.phone_number = self.user.phone_number
            self.is_member = self.user.is_member
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name
    

class ContactMessage(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ResourceCategory(models.Model):
    category = models.CharField(max_length=255, default="Other")

    def __str__(self):
        return self.category
    

class ResourceSubCategory(models.Model):
    subcategory = models.CharField(max_length=255, default="None")
    category = models.ForeignKey(ResourceCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.category.category + "-" + self.subcategory


class ResourceLinkType(models.Model):
    link_type = models.CharField(max_length=255, default="Other")

    def __str__(self):
        return self.link_type


class Resource(models.Model):
    link = models.CharField(max_length=255, default="")

    link_type = models.ForeignKey(ResourceLinkType, on_delete=models.SET_DEFAULT, default=None, null=True)

    category = models.ForeignKey(ResourceCategory, on_delete=models.SET_DEFAULT, default=None, null=True)

    subcategory = models.ForeignKey(ResourceSubCategory, on_delete=models.SET_DEFAULT, default=None, null=True)


    def __str__(self):
        return self.link
    

class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    location = models.CharField(max_length=200)
    event_image = CloudinaryField('Event Image', null=True, blank=True, default='https://res.cloudinary.com/dikcjjfpo/image/upload/v1692796802/mreea-meeting-2_oeygy7.png')
    created_at = models.DateTimeField(auto_now_add=True)

    event_uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    event_short_uuid = models.CharField(max_length=10, unique=True, editable=False, default='')

    resources = models.ManyToManyField(Resource)

    def save(self, *args, **kwargs):
        if not self.event_short_uuid:
            self.event_short_uuid = str(self.event_uuid)[:10]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title