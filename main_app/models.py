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
    

class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    location = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    event_uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    event_short_uuid = models.CharField(max_length=10, unique=True, editable=False, default='')

    def save(self, *args, **kwargs):
        if not self.event_short_uuid:
            self.event_short_uuid = str(self.event_uuid)[:10]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class MemberProfile(models.Model):
    STATE_CHOICES = [
        ('all', 'All States'),
        ('alabama', 'AL - Alabama'),
        ('alaska', 'AK - Alaska'),
        ('arizona', 'AZ - Arizona'),
        ('arkansas', 'AR - Arkansas'),
        ('california', 'CA - California'),
        ('colorado', 'CO - Colorado'),
        ('connecticut', 'CT - Connecticut'),
        ('delaware', 'DE - Delaware'),
        ('florida', 'FL - Florida'),
        ('georgia', 'GA - Georgia'),
        ('hawaii', 'HI - Hawaii'),
        ('idaho', 'ID - Idaho'),
        ('illinois', 'IL - Illinois'),
        ('indiana', 'IN - Indiana'),
        ('iowa', 'IA - Iowa'),
        ('kansas', 'KS - Kansas'),
        ('kentucky', 'KY - Kentucky'),
        ('louisiana', 'LA - Louisiana'),
        ('maine', 'ME - Maine'),
        ('maryland', 'MD - Maryland'),
        ('massachusetts', 'MA - Massachusetts'),
        ('michigan', 'MI - Michigan'),
        ('minnesota', 'MN - Minnesota'),
        ('mississippi', 'MS - Mississippi'),
        ('missouri', 'MO - Missouri'),
        ('montana', 'MT - Montana'),
        ('nebraska', 'NE - Nebraska'),
        ('nevada', 'NV - Nevada'),
        ('new_hampshire', 'NH - New Hampshire'),
        ('new_jersey', 'NJ - New Jersey'),
        ('new_mexico', 'NM - New Mexico'),
        ('new_york', 'NY - New York'),
        ('north_carolina', 'NC - North Carolina'),
        ('north_dakota', 'ND - North Dakota'),
        ('ohio', 'OH - Ohio'),
        ('oklahoma', 'OK - Oklahoma'),
        ('oregon', 'OR - Oregon'),
        ('pennsylvania', 'PA - Pennsylvania'),
        ('rhode_island', 'RI - Rhode Island'),
        ('south_carolina', 'SC - South Carolina'),
        ('south_dakota', 'SD - South Dakota'),
        ('tennessee', 'TN - Tennessee'),
        ('texas', 'TX - Texas'),
        ('utah', 'UT - Utah'),
        ('vermont', 'VT - Vermont'),
        ('virginia', 'VA - Virginia'),
        ('washington', 'WA - Washington'),
        ('west_virginia', 'WV - West Virginia'),
        ('wisconsin', 'WI - Wisconsin'),
        ('wyoming', 'WY - Wyoming'),
    ]

    CATEGORY_CHOICES = [
        ('all', 'ALL Member Categories'),
        ('1', 'Attorney/Legal'),
        ('2', 'Author/Publisher'),
        ('3', 'Course Designer'),
        ('4', 'CPA'),
        ('5', 'Education Director'),
        ('6', 'Inspirational'),
        ('7', 'National Speaker'),
        ('8', 'Online Real Estate School/Educator'),
        ('9', 'Online Training'),
        ('10', 'Professor/Educator'),
        ('11', 'Real Estate Association'),
        ('12', 'Real Estate Regulator'),
        ('13', 'Real Estate School'),
        ('14', 'Real Estate School Owner/Administrator'),
        ('15', 'Trainer/Educator/Instructor'),
        ('16', 'Training Consultant/Coach'),
    ]

    CERTIFICATE_CHOICES = [
        ('any', 'ANY Certifications'),
        ('drei', 'Distinguished Real Estate Instructors (REEA DREI)'),
        ('gsl', 'Gold Standard Leader Certification (REEA GSL)'),
        ('gsi', 'Gold Standard Instructors (GSI)'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, blank=True, default='')
    last_name = models.CharField(max_length=255, blank=True, default='')
    profile_image = CloudinaryField('Profile Image', null=True, blank=True, default='https://res.cloudinary.com/dzwyiggcp/image/upload/v1689692743/MREEA/default-profile-pic_yp9kzz.png')
    profile_image_change = models.CharField(max_length=1000, blank=True, default='')
    display_email = models.BooleanField(default=True)
    personal_email = models.EmailField(blank=True)
    office_email = models.EmailField(blank=True)
    display_number = models.BooleanField(default=True)
    mobile_number = models.CharField(max_length=255, blank=True)
    office_number = models.CharField(max_length=255, blank=True)
    display_address = models.BooleanField(default=True)
    address_line_1 = models.CharField(max_length=255, blank=True)
    address_line_2 = models.CharField(max_length=255, blank=True)
    address_line_3 = models.CharField(max_length=255, blank=True)
    website = models.CharField(max_length=255, blank=True, default='')
    bio = models.TextField(default='', blank=True)
    company_organization = models.CharField(max_length=255, blank=True, default='')
    state = models.CharField(max_length=255, choices=STATE_CHOICES, default='all')
    category = models.CharField(max_length=255, choices=CATEGORY_CHOICES, default='all')
    certificate = models.CharField(max_length=255, choices=CERTIFICATE_CHOICES, default='any')

    short_bio = models.CharField(max_length=80, blank=True, default='')

    is_member = models.BooleanField(default='False')

    def save(self, *args, **kwargs):
        if self.user.is_superuser and not self.user.first_name:
            self.user.first_name = "Admin"
            self.user.save()
        if not self.pk:  # Only set default values for new instances
            self.first_name = self.user.first_name
            self.last_name = self.user.last_name
            self.personal_email = self.user.email
            self.office_email = self.user.email
            self.mobile_number = self.user.phone_number
            self.office_number = self.user.phone_number
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