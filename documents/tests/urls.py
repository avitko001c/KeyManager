from django.conf.urls import include, url

urlpatterns = [
    url(r"^", include("pinax.documents.urls", namespace="documents")),
]
