from __future__ import unicode_literals

import os
import sys
from subprocess import PIPE, Popen

from KeyManager import settings
from django.utils import six
from django.utils.crypto import get_random_string
from django.utils.encoding import DEFAULT_LOCALE_ENCODING, force_text

class CommandError(Exception):
	"""
	Exception class indicating a problem while executing a management
	command.

	If this exception is raised during the execution of a management
	command, it will be caught and turned into a nicely-printed error
	message to the appropriate output stream (i.e., stderr); as a
	result, raising this exception (with a sensible description of the
	error) is the preferred way to indicate that something has gone
	wrong in the execution of a command.
	"""
	pass

def get_json_field(*args, **kwargs):
	if 'postgres' in settings.DATABASES['default']['ENGINE']:
		import django.contrib.postgres.fields as postgres
		JSONField = postgres.JSONField(null=True, blank=True, *args)
	elif 'mysql' in settings.DATABASES['default']['ENGINE']:
		from django_mysql.models import JSONField
		JSONField = JSONField(null=True, blank=True, *args)
	else:
		import jsonfield
		JSONField = jsonfield.JSONField(null=True, blank=True, *args)
	return JSONField

def popen_wrapper(args, os_err_exc_type=CommandError, stdout_encoding='utf-8'):
	"""
	Friendly wrapper around Popen. 
	Borrowed from django.core.managenment.utils
	Returns stdout output, stderr output and OS status code.
	Example:  out, err, status = popen_wrapper(
			['xgettext', '--version'],
			stdout_encoding=DEFAULT_LOCALE_ENCODING,
		  )
	"""
	try:
		p = Popen(args, shell=False, stdout=PIPE, stderr=PIPE, close_fds=os.name != 'nt')
	except OSError as e:
		strerror = force_text(e.strerror, DEFAULT_LOCALE_ENCODING, strings_only=True)
		six.reraise(os_err_exc_type, os_err_exc_type('Error executing %s: %s' %
					(args[0], strerror)), sys.exc_info()[2])
	output, errors = p.communicate()
	return (
		force_text(output, stdout_encoding, strings_only=True, errors='strict'),
		force_text(errors, DEFAULT_LOCALE_ENCODING, strings_only=True, errors='replace'),
		p.returncode
	)

def get_random_secret_key():
	"""
	Borrowed from django.core.managenment.utils
	Return a 50 character random string usable as a SECRET_KEY setting value.
	"""
	chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
	return get_random_string(50, chars)
