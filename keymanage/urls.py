from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from .views import update_profile

from django.views.generic import TemplateView

from django.contrib import admin


urlpatterns = [
	url(r"^$", TemplateView.as_view(template_name="homepage.html"), name="home"),
	url(r"^admin/", admin.site.urls),
	url(r"^account/", include("account.urls")),
	url(r"^profile/", update_profile, name="Profile"),
	url(r"^dbsettings/", include("keymanage-dbsettings.urls")),
	url('^init.js$', include("djrichtextfield.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
