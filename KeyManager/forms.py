# -*- coding: utf-8 -*-

import KeyManager.fields
from KeyManager.fields import *

import KeyManager.widgets
from KeyManager.widgets import *
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from KeyManager.fields import *
from KeyManager.models import Profile, User, UserKey
from KeyManager.constants import ROLE_CHOICES
from KeyManager.widgets import ArrayFieldSelectMultiple, DateWidget
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.widgets import AdminDateWidget
import datetime
import account

class UserForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'email' )

class ProfileForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ('location', 'company', 'birthdate')
	class Media:
		css = {
			"all":  ( "admin/css/widgets.css", "css/app.css", "chosen/css/chosen.css" ) 
		}
		js = ("/jsi18n/", "js/jquery.min.js", "admin/js/jquery.init.js", "admin/js/actions.js", "admin/js/core.js", "admin/js/admin/RelatedObjectLookups.js", 'chosen/js/chosen.jquery.min.js', "chosen/js/chosen.jquery_ready.js", "admin/js/calendar.js", "admin/js/admin/DateTimeShortcuts.js")

	def __init__(self, *args, **kwargs):
		super(ProfileForm, self).__init__(*args, **kwargs)
		this_year = datetime.date.today().year
		years = list(range(this_year-70, this_year+1))
		#years.reverse() # Uncomment this if you want the date rage to start with current
		self.fields["birthdate"].widget = forms.SelectDateWidget(years=years)
	
	def save(self, commit=True):
		user = super(ProfileForm, self).save(commit)
		if commit:
			self.save_m2m()
			return user

class SignupForm(account.forms.SignupForm):
	location = forms.CharField(
		label = _("Location"),
		max_length = 50,
		widget = forms.TextInput()
	)
	company = forms.CharField(
		label = _("Company"),
		max_length = 50,
		widget = forms.TextInput()
	)
	birthdate = forms.DateField(
		label = _("Birthdate"),
		widget = forms.SelectDateWidget(years=range(1910, 2018))
	)

class UserKeyForm(forms.ModelForm):

	class Meta:
		model = UserKey
		fields = ['name', 'key']
		widgets = {
			'name': forms.TextInput(attrs={
				'size': 50,
				'placeholder': "username@hostname, or leave blank to use key comment",
			}),
			'key': forms.Textarea(attrs={
				'cols': 72,
				'rows': 15,
				'placeholder': "Paste in the contents of your public key file here",
			}),
		}

	def get_absolute_url(self):
		from django.urls import reverse
		return reverse('account_sshkeys', args=[str(self.id)])
