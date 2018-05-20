import KeyManager.fields
from KeyManager.fields import *

import KeyManager.widgets
from KeyManager.widgets import *
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from KeyManager.fields import *
from KeyManager.models import Profile, User
from KeyManager.constants import ROLE_CHOICES
from KeyManager.widgets import ArrayFieldSelectMultiple
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.widgets import AdminDateWidget
import account

class UserForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'email' )


class ProfileForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ('location', 'company', 'birthdate')
		#"role" = ChosenModelMultipleChoiceField(queryset=Roles.objects.all())
		widgets = {
			#"role": ChosenSelect( overlay="Select Rold...", choices=ROLE_CHOICES),
			"birthdate": DateWidget()
		}
	class Media:
		css = {
			"all":  ( "admin/css/widgets.css", "css/app.css" ) 
		}
		js = ("/jsi18n/", "js/jquery.min.js", "admin/js/jquery.init.js", "admin/js/actions.js", "admin/js/core.js", "admin/js/admin/RelatedObjectLookups.js", 'chosen/js/chosen.jquery.min.js', "chosen/js/chosen.jquery_ready.js", "admin/js/calendar.js", "admin/js/admin/DateTimeShortcuts.js")

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
