from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.views.i18n import JavaScriptCatalog
from django.contrib import admin
from simplesshkey import views as keyviews
import KeyManager.views
from simplesshkey.views import userkey_edit, userkey_delete, userkey_add

urlpatterns = [
	#url(r"^grappelli/", include("grappelli.urls")),
	url(r'^aws-manager/', include('aws_manager.urls')),
	url(r"^$", TemplateView.as_view(template_name="homepage.html"), name="home"),
 	url(r"^jsi18n/", JavaScriptCatalog.as_view(), name="javascript-catalog"),
	url(r"^admin/", admin.site.urls),
	url(r"^account/", include("account.urls")),
	url(r'account/sshkey/$', keyviews.userkey_list, name='userkey_list'),
	url(r'account/sshkey/add$', keyviews.userkey_add, name='userkey_add'),
	url(r'account/sshkey/(?P<pk>\d+)$', keyviews.userkey_edit, name='userkey_edit'),
	url(r'account/sshkey/(?P<pk>\d+)/delete$', keyviews.userkey_delete, name='userkey_delete'),
	url(r"^account/signup/$", KeyManager.views.SignupView.as_view(), name="account_signup"),
	url(r"^account/profile/$", KeyManager.views.ProfileView.as_view(), name="account_profile"),
	url(r"^dbsettings/", include("dbsettings.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r"^__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns
