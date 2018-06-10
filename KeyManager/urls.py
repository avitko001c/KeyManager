# -*- coding: utf-8 -*-

from django.conf import settings
from django.conf.urls import include, url
from django.urls import path
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.views.i18n import JavaScriptCatalog
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from rest_framework.authtoken import views as rest_framework_views
from KeyManager.sitemaps import StaticViewSitemap
import KeyManager.views as views

sitemaps = {
    "static": StaticViewSitemap,
}

urlpatterns = [
	url(r"^$", views.HomeView.as_view(), name="home"),
	path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap"),
	url(r"^grappelli/", include("grappelli.urls")),
	url(r"^search/?", views.SearchView.as_view(), name="search"),
 	url(r"^jsi18n/", JavaScriptCatalog.as_view(), name="javascript-catalog"),
	url(r"^admin/", admin.site.urls),
	url(r"^docs/", include("pinax.documents.urls", namespace="pinax_documents")),
	url(r"^api-auth/", include("rest_framework.urls")),
	url(r"^account/", include("account.urls")),
	url(r"^account/signup/$", views.SignupView.as_view(), name="account_signup"),
	url(r"^account/profile/$", views.ProfileView.as_view(), name="account_profile"),
	url(r"^account/sshkey/$", views.UserKeyListView.as_view(), name="account_sshkeys"),
	url(r"^account/sshkey/add$", views.userkey_add, name="userkey_add"),
	url(r"^account/sshkey/(?P<pk>\d+)$", views.userkey_edit, name="userkey_edit"),
	url(r"^account/sshkey/(?P<pk>\d+)/delete$", views.userkey_delete, name="userkey_delete"),
	url(r"^account/get_auth_token/$", rest_framework_views.obtain_auth_token, name="get_auth_token"),
	url(r"^dbsettings/", include("dbsettings.urls")),

	### --- SSH Key class based views.....Currently not working --- ###

	#url(r"^account/sshkey/add$", views.UserKeyAddView.as_view(), name="userkey_add"),
	#url(r"^account/sshkey/(?P<pk>\d+)$", views.UserKeyUpdateView.as_view(), name="userkey_edit"),
	#url(r"^account/sshkey/(?P<pk>\d+)$", views.UserKeyDeleteView.as_view(), name="userkey_delete"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r"^__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns
