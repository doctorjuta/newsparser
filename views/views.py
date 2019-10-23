"""List of views for news parser."""
from django.shortcuts import render
from django.views import View


class HomePageView(View):
    """CBV for home page."""

    template_name = "home.html"

    def get(self, request, *args, **kwargs):
        """Home page - get request."""
        return render(
            request,
            self.template_name,
            {
                "title": "Home page"
            }
        )
