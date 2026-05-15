from django.views.generic import View
from django.http.response import HttpResponse

from sfacd.gis.models import Shop2
import json


class GetShopLatLngView(View):
    """
    """
    def post(self, request, *args, **kwargs):
        """
        店舗位置を部分一致で検索し、緯度経度を返す。もし、2店舗以上が見つかった場合はflg=Falseで知らせる
        """
        shop_name = request.POST['shop_name']

        shop_list = Shop2.objects.filter(name__icontains=shop_name, shop_flg=True) #店舗名を部分一致かつ、実店舗で検索
        print(shop_list)
        dict_latlng = {}
        if len(shop_list) == 1:
            dict_latlng['flg'] = True
            dict_latlng['lat'] = shop_list[0].lat
            dict_latlng['lng'] = shop_list[0].lng
        else:
            shop_list = shop_list.filter(shop_kind=1) #検索結果が複数ある場合はトヨペット店舗を優先
            if len(shop_list) == 1:
                dict_latlng['flg'] = True
                dict_latlng['lat'] = shop_list[0].lat
                dict_latlng['lng'] = shop_list[0].lng
            elif len(shop_list) > 1:
                dict_latlng['flg'] = False
                dict_latlng['many'] = True
                shop_names = ''
                for shop in shop_list:
                    shop_names = shop.name + ', ' + shop_names
                dict_latlng['name'] = shop_names
            else:
                dict_latlng['flg'] = False
                dict_latlng['many'] = False
                
        data = json.dumps(dict_latlng)
        print(data)
        return HttpResponse(data, content_type='application/json')
