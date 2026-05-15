from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from sfacd.gis.views.Constant import Constant

class MapsView(LoginRequiredMixin, TemplateView):
    template_name = "gis/maps.html"

    def get(self, request, *args, **kwargs):
        context = super().get_context_data(
            api_key=Constant().FRONT_API
        )
        return super().render_to_response(context)
        