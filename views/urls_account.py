"""List of urls for user account pages."""
from django.urls import path
from .views_account import UserView, UserEditView, UserSubsView


urlpatterns = [
    path("", UserView.as_view(), name="account_home"),
    path("edit/", UserEditView.as_view(), name="account_edit"),
    path("subscriptions/", UserSubsView.as_view(), name="account_subs")
]
