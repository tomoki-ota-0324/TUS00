from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from sfacd.gis.models import Shop, Customer


class CustomerDetailView(LoginRequiredMixin, TemplateView):
    template_name = "gis/customer_detail.html"

    def get(self, request, *args, **kwargs):

        #仮設置
        customer = Customer.objects.get(id=3396)
        
        context = super().get_context_data(
            customer=customer
        )
        return super().render_to_response(context)

