# -*- coding: utf-8 -*-

from django.conf import settings
from django_tables2.utils import A
from KeyManager.models import UserKey
from KeyManager.constants import KEY_TEMPLATE
import django_tables2 as tables

class UserKeyTables(tables.Table):
	if settings.SSHKEY_ALLOW_EDIT:
		key_actions = tables.TemplateColumn(KEY_TEMPLATE, orderable=None)

	class Meta:
		model = UserKey
		template_name = 'django_tables2/bootstrap-responsive.html'
		if settings.SSHKEY_ALLOW_EDIT:
			fields = ('name', 'fingerprint', 'created')
		else:
			fields = ('name', 'fingerprint', 'created', 'last_modified')
