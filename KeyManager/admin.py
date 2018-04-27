from .models import Author, Profile
from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from djrichtextfield.widgets import RichTextWidget

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

class AuthorAdmin(admin.ModelAdmin):
	fields = ('name', 'title', 'view_ssh_key')

	formfield_overrides = {
		models.TextField: {'widget': RichTextWidget},
	}

	def view_ssh_key(self, obj):
		return obj.ssh_key

	view_ssh_key.empty_value_display = '???'

admin.site.unregister(User)

UserAdmin.list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'date_joined', 'is_staff')
Author.list_display = ('ssh_key')

admin.site.register(User, CustomUserAdmin)
admin.site.register(Author, AuthorAdmin)


