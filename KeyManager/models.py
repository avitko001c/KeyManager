from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.contrib.postgres.fields import ArrayField
from KeyManager.constants import ROLE_CHOICES
from KeyManager.fields import *
from KeyManager import settings
import KeyManager.utils as utils

class Role(models.Model):
	role = models.CharField(max_length=255, blank=True)

	def __str__(self): # __unicode__ for Python 2
		return 'Roles for users {}'.format(self.role)

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	location = models.CharField(max_length=30, blank=True)
	company  = models.CharField(max_length=30, blank=True)
	birthdate = models.DateField(null=True, blank=True)
	role = models.CharField(max_length=255, null=True, blank=True)

	def __str__(self):  # __unicode__ for Python 2
		return 'Profile of user: {}'.format(self.user.username)


	@classmethod	
	def get_ssh_keys(name, key):
		"""Get the specific key value for a key. If 
		not found return null."""
		try:
			return name.objects.get(key=key).value
		except:
			return "Null"
			
