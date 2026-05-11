from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.db.models import Q

from sfacd.gis.models import Shop, Customer


class RefineSearchCustomerView(LoginRequiredMixin, TemplateView):
    template_name = "gis/refine_search.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return super().render_to_response(context)

    def get_context_data(self, **kwargs):
        shops = Shop.objects.filter(Q(shop_type=0) | Q(shop_type=1) | Q(shop_type=2)) #部署及び不明以外
        car_types = Customer.objects.values_list('car_type', flat=True).order_by('car_type').distinct() #カスタマーテーブルの車種カラムから重複を除いた車種リストを取得 車種テーブル持つべきか？
        context = super().get_context_data(
            shops=shops,
            car_types=car_types
        )
        return context
