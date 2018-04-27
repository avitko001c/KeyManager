from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class Profile(models.Model):
    DEVOPS = 1
    STANDARD = 2
    ROLE_CHOICES = (
        (DEVOPS, 'DevOps'),
        (STANDARD, 'Standard'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=30, blank=True)
    company  = models.CharField(max_length=30, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, null=True, blank=True)
    ssh_key = models.TextField(blank=True, null=True)

    def __str__(self):  # __unicode__ for Python 2
        return self.user.username

class Author(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=3)
