"""List of urls for news parser."""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import HomePageView, SingleSourcePage, RESTAPIView
from .views import page_about, page_custom_range

urlpatterns = [
    path("account/", include("views.urls_account")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("tinymce/", include("tinymce.urls")),
    path("api/", RESTAPIView.as_view(), name="rest_api"),
    path("", HomePageView.as_view(), name="home_page"),
    path("source/<int:id>/", SingleSourcePage.as_view(), name="single_source"),
    path("about/", page_about, name="about"),
    path("custom_range/", page_custom_range, name="custom_range")
]


if settings.ADMIN_ENABLED:
    urlpatterns.append(path("admin/", admin.site.urls))


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
