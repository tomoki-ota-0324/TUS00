from django.views.generic import TemplateView
from sfacd.gis.views.Constant import Constant
class IndexView(TemplateView):
    template_name = "gis/index.html"
    def get(self, request, *args, **kwargs):
        context = super().get_context_data(
            api_key=Constant().FRONT_API,
        )
        return super().render_to_response(context)
