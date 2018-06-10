from importlib import import_module
from django.apps import apps
from django.urls import path
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.conf import settings
from django.conf.urls import include, url
from django.urls import path
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.views.i18n import JavaScriptCatalog
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from KeyManager.sitemaps import StaticViewSitemap
import KeyManager.views as views
import debug_toolbar

sitemaps = {
    'static': StaticViewSitemap,
}


def get_patterns(app_name, filename):
    app_module = import_module('{}.{}'.format(app_name, filename))
    app_models = apps.get_app_config(app_name).get_models()
    model_names = [model.__name__ for model in app_models]
    patterns = []
    views = []

    for model in model_names:
        for key, value in app_module.__dict__.items():
            if isinstance(value, type):
                if value.__name__.startswith(model):
                    views.append({key: value})
    _views = set()
    for key in views:
        for key, value in key.items():
            for model_name in model_names:
                if value.__name__.startswith(model_name) and\
                            value.__name__ not in _views:
                    if isinstance(value, type):
                        if issubclass(value, ListView):
                            patterns += [path('{}/'.format(
                                model_name.lower()), value.as_view(),
                                name='{}-list'.format(model_name.lower()))]
                        if issubclass(value, DetailView):
                            patterns += [path('{}/<int:pk>/detail/'.format(
                                model_name.lower()), value.as_view(),
                                name='{}-detail'.format(model_name.lower()))]
                        if issubclass(value, CreateView):
                            patterns += [path('{}/create/'.format(
                                model_name.lower()), value.as_view(),
                                name='{}-create'.format(model_name.lower()))]
                        if issubclass(value, UpdateView):
                            patterns += [path('{}/<int:pk>/update/'.format(
                                model_name.lower()), value.as_view(),
                                name='{}-update'.format(model_name.lower()))]
                        if issubclass(value, DeleteView):
                            patterns += [path('{}/<int:pk>/delete/'.format(
                                model_name.lower()), value.as_view(),
                                name='{}-delete'.format(model_name.lower()))]
            _views.add(value.__name__)

    return patterns

# projects is the app name 
# views is the filename with the classbased views of your app 
urlpatterns = get_patterns('KeyManager', 'views') + [
	url(r"^grappelli/", include("grappelli.urls")),
	url(r"^docs/", include("pinax.documents.urls", namespace="pinax_documents")),
	url(r"^account/", include("account.urls")),
	url(r"^dbsettings/", include("dbsettings.urls")),
        url(r"^__debug__/", include(debug_toolbar.urls)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r"^__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns
