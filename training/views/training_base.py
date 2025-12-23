from django.conf import settings

from core.exceptions import WIPFeatureError
from core.views import UnitHubBaseView


class TrainingBaseView(UnitHubBaseView):
    title = "Events"

    def dispatch(self, request, *args, **kwargs):
        if not getattr(settings, "ENABLE_TRAINING", False):
            raise WIPFeatureError
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context["show_management"] = user.is_authenticated and user.is_staff
        context["title"] = self.title

        context["sidebar"] = [
            {"name": "Overview", "path": "/training/"},
            {"name": "Matrix", "path": "/training/matrix/"},
            {"name": "Events", "path": "/events/training/"},
        ]

        if context["show_management"]:
            context["sidebar"].append({"name": "Management", "path": "/training/management/"})

        return context