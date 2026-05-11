from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.db.models import Q
from django.db.models import Prefetch

from sfacd.gis.models import Shop2, Rank, GisCustomer
from sfacd.users.models import User
from sfacd.gis.views.Constant import Constant
from sfacd.gis.views.IndexView import IndexView

# import time


class LargeMapsView(LoginRequiredMixin, TemplateView):
    template_name = "gis/large_maps.html"

    def get(self, request, *args, **kwargs):
        """
        商圏分析画面
        """
        flg = False
        if request.user.department_id in Constant().auth_department_list:
            flg = True
        if flg:
            shops = Shop2.objects.filter(shop_flg=True, shop_kind__in=[1, 2, 3]).order_by('id') # 実店舗かつトヨペット店舗、もしくは、カローラ店舗、ネッツ店舗の場合、マーカー作成の店舗選択肢に入れる（顧客の管轄選択の選択肢、及び店舗位置の表示選択肢）
            other_shops = Shop2.objects.filter(shop_flg=True, shop_kind__in=[4]).order_by('id') # 実店舗かつ候補地の場合のみ（候補地の表示選択肢、選択項目が増えたので分けた）
            ranks = Rank.objects.all()
            current_shop = request.user.shop

            # before_time = time.time()
            # users_ids_list = GisCustomer.objects.filter(shop__shop_flg=True, user__is_active=True).values_list('user_id', flat=True).distinct() #実店舗とアクティブ従業員に紐づく顧客車両から従業員IDのユニークをリストで取得
            # staffs = User.objects.filter(id__in=users_ids_list).order_by('id') #上記の顧客車両を持つ従業員をID降順で取得
            # print('経過時間')
            # print(time.time() - before_time)
            # print(len(staffs))

            context = super().get_context_data(
                api_key=Constant().FRONT_API,
                shops=shops,
                other_shops=other_shops,
                # staffs=staffs,
                current_shop=current_shop,
                ranks=ranks,
            )
            return super().render_to_response(context)
        else:
            error_message = "利用権限が付与されていません。管理者より権限を頂いてください。"
            context = super().get_context_data(
                error_message=error_message
            )
            return super().response_class(
                request=self.request,
                template="gis/index.html",
                context=context,
                using=super().template_engine,
            )
