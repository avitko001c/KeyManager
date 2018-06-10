# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect
from django.views.decorators.http import require_http_methods, require_GET
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.utils.http import is_safe_url
from KeyManager.tables import UserKeyTables
from django_tables2 import SingleTableView
from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render, render_to_response
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView
from django.views.generic.edit import FormView, UpdateView, DeleteView, CreateView
from KeyManager.forms import ProfileForm, UserForm, UserKeyForm
from account.compat import is_authenticated
from account.forms import (
	ChangePasswordForm,
	LoginUsernameForm,
	PasswordResetForm,
	PasswordResetTokenForm,
	SettingsForm,
	SignupForm,
)
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
from KeyManager.models import UserKey, Profile

### Class Based Views ###
class HomeView(TemplateView):
	template_name="homepage.html"

	def get_context_data(self, **kwargs):
		ctx = super(HomeView, self).get_context_data(**kwargs)
		ctx.update({})
		return ctx

class SearchView(TemplateView):
	template_name = "search.html"

	def get_context_data(self, **kwargs):
		ctx = super(SearchView, self).get_context_data(**kwargs)
		ctx.update({})
		return ctx

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
	form_kwargs = {}
	messages = { "profile_updated": {
		"level": messages.SUCCESS,
		"text": _("Profile Updated.")
	   		 },
	}

	def get(self, *args, **kwargs):
		return super(ProfileView, self).get(*args, **kwargs)

	def post(self, *args, **kwargs):
		return super(ProfileView, self).post(*args, **kwargs)
	
	def get_form_class(self):
		return super(ProfileView, self).get_form_class()

	def get_user(self):
		return self.request.user

	def get_initial(self):
		initial = super(ProfileView, self).get_initial()	
		initial["profile"] = self.request.user.profile
		return initial

	def get_form_kwargs(self):
		#kwargs = {"initial": self.get_initial()}
		kwargs = super(ProfileView, self).get_form_kwargs()
		kwargs.update(self.form_kwargs)
		return kwargs

	def form_valid(self, form):
		#self.update_profile(form)
		form.save(commit=False) # get just the object but don't commit it yet.
		form.save_m2m()
		if self.messages.get("profile_updated"):
			messages.add_message(
				self.request,
				self.messages["profile_updated"]["level"],
				self.messages["profile_updated"]["text"]
			)
		return super(ProfileView,self).form_valid(form)
		#return redirect(self.get_success_url())

	def update_profile(self, form):
		self.update_fields(form)

	def get_context_data(self, **kwargs):
		ctx = super(ProfileView, self).get_context_data(**kwargs)
		redirect_field_name = self.get_redirect_field_name()
		ctx.update({
			"redirect_field_name": redirect_field_name,
			"redirect_filed_value": self.request.POST.get(redirect_field_name, 
						self.request.GET.get(redirect_field_name, 
						"")),
			})
		return ctx

	def update_fields(self, form):
		fields = {}
		if "location" in form.cleaned_data:
			fields["location"] = form.cleaned_data["location"].split()
		if "company" in form.cleaned_data:
			fields["company"] = form.cleaned_data["company"].split()
		if "birthdate" in form.cleaned_data:
			fields["birthdate"] = form.cleaned_data["birthdate"]
		if fields:
			profile = self.request.user.profile
			for l, c, b in fields.items():
				setattr(profile, l, c, b)
			profile.save()

	def get_redirect_field_name(self):
		return self.redirect_field_name

	def get_success_url(self, fallback_url=None, **kwargs):
		if fallback_url is None:
			fallback_url = settings.ACCOUNT_SETTINGS_REDIRECT_URL
		kwargs.setdefault("redirect_field_name", self.get_redirect_field_name())
		return default_redirect(self.request, fallback_url, **kwargs)

#class UserKeyAddView(CreateView):
#	model = UserKey
#	fields = ['name', 'key']
#	template_name = "account/userkey_add.html"
#	messages = { "sshkey_added": {
#		"level": messages.SUCCESS,
#		"text": _("UserKey Added.")
#	   		 },
#	}
#	
#	def post(self, request):
#                userkey = UserKey(user=request.user)
#                userkey.request = request
#                form = UserKeyForm(request.POST, instance=userkey)
#
#        def form.valid(self, request):
#                        form.save()
#                        default_redirect = reverse('account_sshkeys')
#                        url = request.GET.get('next', default_redirect)
#                        if not is_safe_url(url=url, host=request.get_host()):
#                                url = default_redirect
#                        message = 'SSH public key %s was added.' % userkey.name
#                        messages.success(request, message, fail_silently=True)
#                        return redirect(url)
#	
#	def get(self, request):
#		 form = UserKeyForm()
#
#	def get_success_url(self, request):
#		return render(request, 'account/userkey_detail.html',
#                                  context={'form': form, 'action': 'add'})

class UserKeyListView(SingleTableView):
	model = UserKey
	template_name = "account/userkey_list.html"
	table_class = UserKeyTables

	
#class UserKeyUpdateView(UpdateView):
#	model = UserKey
#	template_name = "account/userkey_detail.html"
#	success_url = 'account/sshkey/'
#	messages = { "sshkey_updated": {
#		"level": messages.SUCCESS,
#		"text": _("SSH Key Updated.") },
#	}

#class UserKeyDeleteView(DeleteView):
#	model = UserKey
#	form_class = UserKeyForm
#	template_name = "account/userkey_delete.html"
#
#	def form_valid(self, form):
#		self.form.save(form)
#		if self.messages.get("sshkey_deleted"):
#			messages.add_message(
#				self.request,
#				self.messages["sshkey_deleted"]["level"],
#				self.messages["profile_deleted"]["text"]
#			)
#		return redirect(self.get_success_url())
#
#	#def get_success_url(self):
#		#return reverse("account_sshkeys")
#
##### Views ####

@login_required
@require_http_methods(['GET', 'POST'])
def userkey_add(request):
	if request.method == 'POST':
		userkey = UserKey(user=request.user)
		userkey.request = request
		form = UserKeyForm(request.POST, instance=userkey)
		if form.is_valid():
			form.save()
			default_redirect = reverse('account_sshkeys')
			url = request.GET.get('next', default_redirect)
			if not is_safe_url(url=url, host=request.get_host()):
				url = default_redirect
			message = 'SSH public key %s was added.' % userkey.name
			messages.success(request, message, fail_silently=True)
			return HttpResponseRedirect(url)
	else:
		form = UserKeyForm()
	return render(request, 'account/userkey_detail.html',
				  context={'form': form, 'action': 'add'})


@login_required
@require_http_methods(['GET', 'POST'])
def userkey_edit(request, pk):
	if not settings.SSHKEY_ALLOW_EDIT:
		raise PermissionDenied
	userkey = get_object_or_404(UserKey, pk=pk)
	if userkey.user != request.user:
		raise PermissionDenied
	if request.method == 'POST':
		form = UserKeyForm(request.POST, instance=userkey)
		if form.is_valid():
			form.save()
			default_redirect = reverse('account_sshkeys')
			url = request.GET.get('next', default_redirect)
			if not is_safe_url(url=url, host=request.get_host()):
				url = default_redirect
			message = 'SSH public key %s was saved.' % userkey.name
			messages.success(request, message, fail_silently=True)
			return HttpResponseRedirect(url)
	else:
		form = UserKeyForm(instance=userkey)
	return render(request, 'account/userkey_detail.html',
				  context={'form': form, 'action': 'edit'})


@login_required
@require_GET
def userkey_delete(request, pk):
	userkey = get_object_or_404(UserKey, pk=pk)
	if userkey.user != request.user:
		raise PermissionDenied
	userkey.delete()
	message = 'SSH public key %s was deleted.' % userkey.name
	messages.success(request, message, fail_silently=True)
	return HttpResponseRedirect(reverse('account_sshkeys'))

