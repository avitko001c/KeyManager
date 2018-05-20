import os

from django.apps import apps
from django.conf import settings

INTERNAL_IPS = [
	"127.0.0.1",
	"localhost",
]

USE_SITES = True
USE_CACHE = True

CACHES = {
	'default': {
		'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
		'LOCATION': '/var/tmp/django_cache',
	}
}

VALUE_LENGTH = 255

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
PACKAGE_ROOT = os.path.abspath(os.path.dirname(__file__))
BASE_DIR = PACKAGE_ROOT

DEBUG = True

GRAPPELLI_INDEX_DASHBOARD = 'Sparta.dashboard.CustomIndexDashboard'

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.postgresql_psycopg2',
		'NAME': 'keymanager',
		'USER': 'andrew.vitko',
		'PASSWORD': 'Lisa07!@',
		'HOST': 'localhost',
		'PORT': '',
	}
}


ALLOWED_HOSTS = [
	"localhost",
]

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = "UTC"

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = "en-us"

SITE_ID = int(os.environ.get("SITE_ID", 1))

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(PACKAGE_ROOT, "site_media", "media")

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = "/site_media/media/"

# Absolute path to the directory static files should be collected to.
# Don"t put anything in this directory yourself; store your static files
# in apps" "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PACKAGE_ROOT, "site_media", "static")

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = "/site_media/static/"

# Additional locations of static files
STATICFILES_DIRS = [
	os.path.join(PROJECT_ROOT, "static", "dist"),
]

STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = [
	"django.contrib.staticfiles.finders.FileSystemFinder",
	"django.contrib.staticfiles.finders.AppDirectoriesFinder",
	"django_assets.finders.AssetsFinder",
]

# Make this unique, and don't share it with anybody.
SECRET_KEY = "lhiss+z7-wcksc%bavg_f9gvko-gnlv_$m-!woax_kv_4he*_u"

TEMPLATES = [
	{
		"BACKEND": "django.template.backends.django.DjangoTemplates",
		"DIRS": [
			os.path.join(PACKAGE_ROOT, "templates"),
		],
		"APP_DIRS": True,
		"OPTIONS": {
			"debug": DEBUG,
			"context_processors": [
				"django.template.context_processors.request",
				"django.contrib.auth.context_processors.auth",
				"django.template.context_processors.debug",
				"django.template.context_processors.i18n",
				"django.template.context_processors.media",
				"django.template.context_processors.static",
				"django.template.context_processors.tz",
				"django.template.context_processors.request",
				"django.contrib.messages.context_processors.messages",
				"pinax_theme_bootstrap.context_processors.theme",
				"account.context_processors.account",
				"KeyManager.context_processors.settings"
			],
		},
	},
]

MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'

MIDDLEWARE = [
	"django.contrib.sessions.middleware.SessionMiddleware",
	"django.middleware.common.CommonMiddleware",
	"django.middleware.csrf.CsrfViewMiddleware",
	"django.contrib.auth.middleware.AuthenticationMiddleware",
	"debug_toolbar.middleware.DebugToolbarMiddleware",
	"django.contrib.messages.middleware.MessageMiddleware",
	"django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "KeyManager.urls"

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = "KeyManager.wsgi.application"

INSTALLED_APPS = [
	"django_assets",
	"django.contrib.admin",
	"django.contrib.auth",
	"django.contrib.contenttypes",
	"django.contrib.messages",
	"django.contrib.sessions",
	"django.contrib.sites",
	"django.contrib.staticfiles",
	"django.contrib.postgres",
	"debug_toolbar",
	#"grappelli.dashboard",
	#"grappelli",

	# templates
	"pinax_theme_bootstrap",
	"bootstrapform",
	"pinax.templates",

	# external
	"pinax.eventlog",
	"pinax.webanalytics",
	"account",
	"aws_manager",

	# project
	"simplesshkey",
	"KeyManager",
	"dbsettings",
]

ADMIN_URL = "admin:index"
CONTACT_EMAIL = "support@example.com"

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
	"version": 1,
	"disable_existing_loggers": False,
	"filters": {
		"require_debug_false": {
			"()": "django.utils.log.RequireDebugFalse"
		}
	},
	"handlers": {
		"mail_admins": {
			"level": "ERROR",
			"filters": ["require_debug_false"],
			"class": "django.utils.log.AdminEmailHandler"
		}
	},
	"loggers": {
		"django.request": {
			"handlers": ["mail_admins"],
			"level": "ERROR",
			"propagate": True,
		},
	}
}

FIXTURE_DIRS = [
	os.path.join(PROJECT_ROOT, "fixtures"),
]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

ACCOUNT_OPEN_SIGNUP = True
ACCOUNT_EMAIL_UNIQUE = True
ACCOUNT_EMAIL_CONFIRMATION_REQUIRED = False
ACCOUNT_LOGIN_REDIRECT_URL = "home"
ACCOUNT_LOGOUT_REDIRECT_URL = "home"
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 2
ACCOUNT_USE_AUTH_AUTHENTICATE = True

AUTHENTICATION_BACKENDS = [
	"account.auth_backends.UsernameAuthenticationBackend",
]

SSHKEY_ALLOW_EDIT = True

SSHKEY_AUTHORIZED_KEYS_OPTIONS = "" 

SSHKEY_DEFAULT_HASH = "md5"
