from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from sfacd.gis.models import Shop, Customer


class FavouriteListView(LoginRequiredMixin, TemplateView):
    template_name = "gis/favourite_list.html"

    def get(self, request, *args, **kwargs):
        customers = Customer.objects.filter(staff_id=request.user.id, rank_kind="SS")
        context = super().get_context_data(
            customers=customers
        )
        return super().render_to_response(context)

