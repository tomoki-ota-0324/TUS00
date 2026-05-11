from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "gis/dashboard.html"

    def get(self, request, *args, **kwargs):
        context = super().get_context_data()
        return super().render_to_response(context)
        