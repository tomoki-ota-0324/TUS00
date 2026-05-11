from django.views.generic import TemplateView

class IndexView(TemplateView):
    template_name = "gis/index.html"

    def get(self, request, *args, **kwargs):
        context = super().get_context_data()
        return super().render_to_response(context)
        