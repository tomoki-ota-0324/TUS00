from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.http.response import HttpResponse

from sfacd.gis.views.Constant import Constant
from sfacd.gis.models import Shop, Customer, Mylist

import json


class DetailAttackListView(LoginRequiredMixin, TemplateView):
    template_name = "gis/detail_attack.html"

    def get(self, request, *args, **kwargs):
        mylist = Mylist.objects.filter(user_id=request.user.id)

        
        current_list = Mylist.objects.latest('modify_date') #更新日時で最新のもの
        customers = current_list.customers.all()
        current_shop = Shop.objects.get(id=request.user.shop_id)
        print(current_shop)

        context = self.get_context_data()
        context['mylist'] = mylist
        context['current_list'] = current_list
        context['customers'] = customers
        context['current_shop'] = current_shop
        return super().render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(
            api_key=Constant().FRONT_API,
        )
        return context

    def post(self, request, *args, **kwargs):
        """
        現在表示されているマイリストの顧客をすべて返す
        """
        print(request.POST)
        mylist_id = request.POST['mylist_id']
        current_mylist = Mylist.objects.get(id=mylist_id)
        customers = current_mylist.customers.all()
        customers = customers.extra(select={'last_contact_date': "DATE_FORMAT(last_contact_date, '%%Y-%%m-%%d')"}) #jsonに変換するため、date formatをstrに変換してDBから取得するクエリを発行
        customers = list(customers.values('address', 'rank_kind', 'car_type', 'last_contact_date')) #QuerySetから特定のカラムのみの辞書のリストに変換
        responce_dict = {
            #　以下コメントアウトはすべてサーバー側の処理に切り替えるときに使用
            # "draw": request.POST['draw'],
            # "recordsTotal": len(customers),
            # "recordsFiltered": len(customers),
            "data": customers,
        }

        data = json.dumps(responce_dict)
        # data = serializers.serialize('json', responce_dict)
        print(data)
        return HttpResponse(data, content_type='application/json')
        