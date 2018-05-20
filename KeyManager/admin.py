from KeyManager.models import Role, Profile
from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

class ProfileInline(admin.StackedInline):
	model = Profile
	can_delete = False
	verbose_name_plural = 'Profile'
	fk_name = 'user'

class CustomUserAdmin(UserAdmin):
	inlines = (ProfileInline, )
	list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'date_joined', 'is_staff', 'get_location')
	list_selected_related = ('profile')
	def get_location(self, instance):
		return instance.profile.location
	get_location.short_description = 'Location'

	def get_inline_instances(self, request, obj=None):
		if not obj:
			return list()
		return super(CustomUserAdmin, self).get_inline_instances(request, obj)

class RoleAdmin(admin.ModelAdmin):
	fields = ['role']
	list_display = ['role']
	list_selected_related = ('role')
	model = Role
	can_delete = True
	verbose_name_plural = 'Role'
	fk_name = 'role'
	formfield_overrides = {}

admin.site.unregister(User)

UserAdmin.list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'date_joined', 'is_staff')

admin.site.register(User, CustomUserAdmin)
admin.site.register(Role, RoleAdmin)


