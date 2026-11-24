"""Root URL configuration: the admin site plus every page of the Samsung_App."""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("Samsung_App.urls")),
]
