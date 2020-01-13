"""List of urls for user account pages."""
from django.urls import path
from django.contrib.auth.views import PasswordResetView
from .views_account import UserView, UserEditView, UserSubsView, UserNew


urlpatterns = [
    path("", UserView.as_view(), name="account_home"),
    path("edit/", UserEditView.as_view(), name="account_edit"),
    path("subscriptions/", UserSubsView.as_view(), name="account_subs"),
    path("new/", UserNew.as_view(), name="account_new"),
    path("reset_password/", PasswordResetView.as_view(), name="account_rpass")
]
