"""List of views for user profiles."""
from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from .forms import SignUpForm


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


class UserNew(View):
    """CBV for creating new users."""

    template_name ="account/new-user.html"

    def get(self, request, *args, **kwargs):
        """New user page - get request."""
        if request.user.is_authenticated:
            return HttpResponseRedirect("/")
        form = SignUpForm()
        data = {
            "title": "Реєстрація",
            "form": form
        }
        return render(
            request,
            self.template_name,
            data
        )

    def post(self, request, *args, **kwargs):
        """New user page - post request."""
        form = SignUpForm(request.POST)
        if form.is_valid():
            useremail = form.cleaned_data.get("email")
            with_same_email = User.objects.filter(email=useremail)
            if with_same_email:
                form.add_error("email", "Цей email вже зареєстрований.")
            else:
                form.save()
                username = form.cleaned_data.get("username")
                raw_password = form.cleaned_data.get("password1")
                user = authenticate(username=username, password=raw_password)
                login(request, user)
                return HttpResponseRedirect("/")
        data = {
            "title": "Реєстрація",
            "form": form
        }
        return render(
            request,
            self.template_name,
            data
        )
