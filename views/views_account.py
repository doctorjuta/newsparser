"""List of views for user profiles."""
from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseBadRequest
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User


class UserView(LoginRequiredMixin, View):
    """CBV for personal accounnt page."""

    def get(self, request, *args, **kwargs):
        """Account page - get request."""
        data = {
            "title": "Особистий кабінет"
        }
        template_name = "account/profile-home.html"
        return render(
            request,
            template_name,
            data
        )


class UserEditView(LoginRequiredMixin, View):
    """CBV for personal accounnt page - edit section."""

    template_name ="account/profile-edit.html"

    def get(self, request, *args, **kwargs):
        """Edit account page - get request."""
        data = {
            "title": "Редагувати профіль"
        }
        return render(
            request,
            self.template_name,
            data
        )

    @method_decorator(csrf_protect)
    def post(self, request, *args, **kwargs):
        """Edit account page - post request."""
        if "user_id" not in request.POST:
            return HttpResponseBadRequest(
                "User ID wasn't provide."
            )
        try:
            current_user = User.objects.get(pk=request.POST["user_id"])
        except ObjectDoesNotExist:
            return HttpResponseBadRequest(
                "Invalid User ID."
            )
        current_user.first_name = request.POST["first_name"]
        current_user.last_name = request.POST["last_name"]
        current_user.email = request.POST["email"]
        current_user.save()
        data = {
            "title": "Редагувати профіль",
            "user": current_user,
            "message": "Профіль успішно змінено"
        }
        return render(
            request,
            self.template_name,
            data
        )


class UserSubsView(LoginRequiredMixin, View):
    """CBV for personal accounnt page - email subscriptions section."""

    template_name ="account/profile-subs.html"

    def get(self, request, *args, **kwargs):
        """Subscriptions page - get request."""
        data = {
            "title": "Email розсилка"
        }
        return render(
            request,
            self.template_name,
            data
        )
