from django.conf import settings
from dbsettings.utils import set_defaults
from KeyManager import models as keyapp

set_defaults(keyapp,
	('SSHKEY', 'allow_edit', True)
	('SSHKEY', 'default_hash', md5)
)
