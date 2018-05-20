# -*- coding: utf-8 -*-
from importlib import import_module

from django.apps import AppConfig as BaseAppConfig
from django.utils.translation import ugettext_lazy as _

class AppConfig(BaseAppConfig):

    name = "KeyManager"
    verbose_name = _(u'KeyManager')

    def ready(self):
        import_module("KeyManager.receivers")
