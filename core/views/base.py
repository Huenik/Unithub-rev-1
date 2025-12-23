from django.conf import settings
from django.views.generic import TemplateView
from django.contrib import messages

class UnitHubBaseView(TemplateView):
    title = "UnitHub"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context["show_management"] = user.is_authenticated and user.is_staff

        nav_links = [
            {"name": "Dashboard", "url": "/"},
            {"name": "ORBAT", "url": "/orbat/"},
            {"name": "Events", "url": "/events/"},
            {"name": "Training", "url": "/training/"},
        ]

        # TODO Remove once WIP has been finished
        # Filter nav links based on settings
        if not getattr(settings, "ENABLE_EVENTS", False):
            nav_links = [link for link in nav_links if link["name"] != "Events"]

        if not getattr(settings, "ENABLE_TRAINING", False):
            nav_links = [link for link in nav_links if link["name"] != "Training"]

        context["nav_links"] = nav_links

        # Default breadcrumbs (can be overridden in child views)
        context.setdefault("breadcrumbs", [])

        context["title"] = self.title
        # Theme can be set in session or user preference
        context["theme"] = getattr(user, "theme", "theme-light")

        return context

    def add_message(self, message, level=messages.INFO):
        """
        Helper to add a message prompt to the user.
        Can be called from any view inheriting this base.
        """
        messages.add_message(self.request, level, message)