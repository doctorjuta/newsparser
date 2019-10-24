"""List of urls for news parser."""
from django.contrib import admin
from django.urls import path, include
from .views import HomePageView, RESTAPIView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("api/", RESTAPIView.as_view(), name="rest_api"),
    path("", HomePageView.as_view(), name="home_page"),
]
