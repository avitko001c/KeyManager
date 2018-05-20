from __future__ import unicode_literals


from django import forms
from django.db import transaction, models
from django.contrib import auth, messages
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponseForbidden
from django.template import RequestContext
from django.template.context_processors import csrf
from django.shortcuts import get_object_or_404, redirect, render, render_to_response
from django.utils.decorators import method_decorator
from django.utils.http import base36_to_int, int_to_base36
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic.edit import FormView
from .forms import ProfileForm, UserForm
from account import signals
from account.compat import is_authenticated, reverse
from account.conf import settings
from account.forms import (
	ChangePasswordForm,
	LoginUsernameForm,
	PasswordResetForm,
	PasswordResetTokenForm,
	SettingsForm,
	SignupForm,
)
from account.hooks import hookset
from account.mixins import LoginRequiredMixin
from account.models import (
	Account,
	AccountDeletion,
	EmailAddress,
	EmailConfirmation,
	PasswordHistory,
	SignupCode,
)
from account.utils import default_redirect, get_form_data
import account.views
import KeyManager.forms

class SignupView(account.views.SignupView):
	form_class = SignupForm

	def after_signup(self, form):
		self.save_profile(form)
		super(SignupView, self).after_signup(form)

	def save_profile(self, form):
		profile = self.created_user.profile  # replace with your reverse one-to-one profile attribute
		profile.location = form.cleaned_data["location"]
		profile.company  = form.cleaned_data["company"]
		profile.birthdate = form.cleaned_data["birthdate"]
		profile.save()


class ProfileView(FormView):
	template_name = "account/profile.html"
	form_class = ProfileForm
	redirect_field_name = "next"
	messages = {
	     "profile_updated": {
		"level": messages.SUCCESS,
		"text": _("Profile Updated.")
       	     },
	}
	
	def get_form_class(self):
		self.primary_email_address = EmailAddress.objects.get_primary(self.request.user)
		return super(ProfileView, self).get_form_class()

	def get_initial(self):
		initial = super(ProfileView, self).get_initial()	
		initial["profile"] = self.request.user.profile
		return initial

	def form_valid(self, form):
		self.update_profile(form)
		if self.messages.get("profile_updated"):
			messages.add_message(
				self.request,
				self.messages["profile_updated"]["level"],
				self.messages["profile_updated"]["text"]
			)
		return redirect(self.get_success_url())

	def update_profile(self, form):
		self.update_fields(form)
		self.update_keys(form)

	def update_keys(self, form, **kwargs):
		user = self.request.user
		# @@@ handle multiple keys per user
		keys = "undef" #future work needed to update keys in database

	def get_ssh_keys(self, form, **kwargs):
		user = self.request.user
		keys = "undef" #future work needed to grab keys from database

	def get_context_data(self, **kwargs):
		ctx = super(ProfileView, self).get_context_data(**kwargs)
		redirect_field_name = self.get_redirect_field_name()
		ctx.update({
			"redirect_field_name": redirect_field_name,
			"redirect_filed_value": self.request.POST.get(redirect_field_name, self.request.GET.get(redirect_field_name, "")),
		})
		return ctx

	def update_fields(self, form):
		fields = {}
		if "location" in form.cleaned_data:
			fields["location"] = forms.cleaned_data["location"]
		if "company" in form.cleaned_data:
			fields["company"] = forms.cleaned_data["company"]
		if "role" in form.cleaned_data:
			fields["role"] = forms.cleaned_data["role"]
		if "birthdate" in form.cleaned_data:
			fields["birthdate"] = forms.cleaned_data["birthdate"]
		if fields:
			profile = self.request.user.profile
			for k, v in fields.items():
				setattr(profile, k, v)
			profile_form.save()

	def get_redirect_field_name(self):
		return self.redirect_field_name

	def get_success_url(self, fallback_url=None, **kwargs):
		if fallback_url is None:
			fallback_url = settings.ACCOUNT_SETTINGS_REDIRECT_URL
		kwargs.setdefault("redirect_field_name", self.get_redirect_field_name())
		return default_redirect(self.request, fallback_url, **kwargs)


def group_and_bridge(kwargs):
	"""
	Given kwargs from the view (with view specific keys popped) pull out the
	bridge and fetch group from database.
	"""

	bridge = kwargs.pop("bridge", None)

	if bridge:
		try:
			group = bridge.get_group(**kwargs)
		except ObjectDoesNotExist:
			raise Http404
	else:
		group = None

	return group, bridge


def group_context(group, bridge):
	# @@@ use bridge
	return {
		"group": group,
	}

@login_required
@transaction.atomic
def update_profile(request, **kwargs):
	form_class = kwargs.pop("form_class", ProfileForm)
	user_form_class = kwargs.pop("form_class", UserForm)
	#key_form_class = kwargs.pop("form_class", KeyForm)
	template_name = kwargs.pop("template_name", "account/profile.html")
	group, bridge = group_and_bridge(kwargs)
	ctx = group_context(group, bridge)

	if request.method == 'POST':
		user_form = user_form_class(request.POST, instance=request.user)
		#key_form = key_form_class(request.POST, instance=request.user.keys)
		profile_form = form_class(request.POST, instance=request.user.profile)
		if user_form.is_valid() and profile_form.is_valid():
			user_form.save()
			profile_form.save()
			#key_form.save()
			messages.add_message(request, messages.SUCCESS,
				_(u"Profile successfully updated.")
			)
			return redirect('/account/settings')
		else:
			messages.add_message(request, messages.ERROR,
				_(u"Please correct the error below.")
			)
	else:
		user_form = UserForm(instance=request.user)
		profile_form = ProfileForm(instance=request.user.profile)
		#key_form = ProfileForm(instance=request.user.keys)
	ctx.update({
		"user_form": user_form,
		'profile_form': profile_form,
	})
	ctx.update(csrf(request))
	return render_to_response(template_name, RequestContext(request, ctx))
