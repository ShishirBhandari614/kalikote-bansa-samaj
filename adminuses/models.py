from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError




class User(AbstractUser):
    ROLE_CHOICES = (
        ('superadmin', 'Super Admin'),
        ('subadmin', 'Sub Admin'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def is_superadmin(self):
        return self.role == 'superadmin'

    def is_subadmin(self):
        return self.role == 'subadmin'


# Model for Photo upload
class Photo(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='photos/')
    description = models.TextField(blank=True)
    date = models.DateField()

    def __str__(self):
        return self.title

# Model for Video upload
class Video(models.Model):
    title = models.CharField(max_length=100)
    video_file = models.FileField(upload_to='videos/')
    description = models.TextField(blank=True)
    date = models.DateField()

    def __str__(self):
        return self.title

class Logo(models.Model):
    logo = models.ImageField(upload_to='logos/')


    
    def save(self, *args, **kwargs):
        """Ensure only one Logo instance exists; update if already present."""
        if not self.pk and Logo.objects.exists():
            # There is already a logo, update it instead of creating a new row
            existing = Logo.objects.first()
            existing.logo = self.logo
            existing.save()
        else:
            # No logo exists or updating the existing one
            super().save(*args, **kwargs)

    def __str__(self):
        return "Site Logo"


class Members(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='members/')
    position = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Slide(models.Model):
    image = models.ImageField(upload_to='slides/')
    caption = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.caption[:50] if self.caption else "Slide"
