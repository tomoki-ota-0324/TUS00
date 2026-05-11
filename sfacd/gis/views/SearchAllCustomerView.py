from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.http.response import HttpResponse
# from django.core import serializers

from sfacd.gis.models import CustomerCars
from sfacd.gis.views.MainMapView import MainMapView
import json
from distutils.util import strtobool #文字列から真偽値への変換

class SearchAllCustomerView(LoginRequiredMixin, View):
    """
    """
    def post(self, request, *aegs, **kwargs):
        """
        ログインユーザーの顧客全てを返す
        絞込検索がされていれば、絞込後の顧客のみ返す
        """
        print(request.POST)
        refine_flg = request.POST['refine_flg']
        if strtobool(refine_flg): #もし検索条件が設定されているなら
            print("検索条件追加リスト表示")
            customers = MainMapView().post(request)
        else:
            print("初期リスト表示")
            customers = CustomerCars.objects.filter(user_id=request.user.id).select_related().order_by('id')

        customers = customers.extra(select={'inspection_date': "DATE_FORMAT(inspection_date, '%%Y-%%m-%%d')"}) #jsonに変換するため、date formatをstrに変換してDBから取得するクエリを発行
        customers = list(customers.values('base_customer__id', 'base_customer__name', 'base_customer__customerdetail__name_kana', 'rank__rank', 'base_customer__address', 'car__name', 'inspection_date', 'shop__name', 'user__name')) #QuerySetから特定のカラムのみの辞書のリストに変換
        responce_dict = {
            #　以下コメントアウトはすべてサーバー側の処理に切り替えるときに使用
            # "draw": request.POST['draw'],
            # "recordsTotal": len(customers),
            # "recordsFiltered": len(customers),
            "data": customers,
        }

        data = json.dumps(responce_dict)
        # data = serializers.serialize('json', responce_dict)
        print("リストのデータ")
        print(data)
        return HttpResponse(data, content_type='application/json')

