from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

class ChartsView(LoginRequiredMixin, TemplateView):
    template_name = "gis/charts.html"

    def get(self, request, *args, **kwargs):
        context = super().get_context_data()
        return super().render_to_response(context)
        