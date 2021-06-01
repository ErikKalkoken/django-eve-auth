from django.urls import include, path

urlpatterns = [
    path("sso/", include("eve_auth.urls")),
]
