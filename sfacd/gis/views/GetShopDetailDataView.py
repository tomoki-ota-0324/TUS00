from django.views.generic import View
# from django.db.models import Q
from django.http.response import HttpResponse
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist

from sfacd.gis.models import Shop2
# from sfacd.users.models import User
# import geojson
import json


class GetShopDetailDataView(View):

    def post(self, request, *args, **kwargs):
        """
        送られてきた店舗IDよりその店舗の詳細データをjson形式で返す
        """
        shop_id = request.POST['shop_id'] #店舗Id

        try:
            shop = Shop2.objects.get(id=shop_id)
            dict_shop1 = shop.__dict__
            dict_shop2 = shop.shop_detail.__dict__
            del dict_shop1['_state'] #ModelStateObject 削除
            del dict_shop2['_state'] #ModelStateObject 削除
            dict_shop1.update(dict_shop2) #辞書の結合
            dict_shop1['data'] = True #詳細データが取得できたときのフラグ
            num_key_list = ['Y_1', 'Y_2', 'Y_3', 'building_area', 'chinshaku_area', 'floor_area', 'members', 'shop_area']
            for key in dict_shop1:
                if key in num_key_list:
                    if dict_shop1[key] is None:
                        dict_shop1[key] = "0"
                    else:
                        dict_shop1[key] = dict_shop1[key].replace(' ', '') #特定のカラムのみ空白を除去する
                        dict_shop1[key] = dict_shop1[key].replace('\u3000', '') #特定のカラムのみ全角空白を除去する
            #カラムに複数データ格納しているものをカンマで分割してリスト出力し、それぞれの要素にキーを与えて辞書に格納
            shop_area_list = dict_shop1['shop_area'].split(',')
            if len(shop_area_list) == 2:
                dict_shop1['shop_area_square_meter'] = shop_area_list[0]
                dict_shop1['shop_area_tsubo'] = shop_area_list[1]
            chinshaku_area_list = dict_shop1['chinshaku_area'].split(',')
            if len(chinshaku_area_list) == 2:
                dict_shop1['chinshaku_area_square_meter'] = chinshaku_area_list[0]
                dict_shop1['chinshaku_area_tsubo'] = chinshaku_area_list[1]
            building_area_list = dict_shop1['building_area'].split(',')
            if len(building_area_list) == 2:
                dict_shop1['building_area_square_meter'] = building_area_list[0]
                dict_shop1['building_area_tsubo'] = building_area_list[1]
            floor_area_list = dict_shop1['floor_area'].split(',')
            if len(floor_area_list) == 2:
                dict_shop1['total_floor_area_square_meter'] = floor_area_list[0]
                dict_shop1['total_floor_area_tsubo'] = floor_area_list[1]
            members = dict_shop1['members'].split(',')
            if len(members) == 11:
                members_list = ['total_shop_menber', 'store_manager', 'vice_store_manager', 'TM', 'QA_SC', 'STM', 'SAD_TM', 'EL_WSL', 'SE_TS', 'FC_RS', 'others']
                n = 0
                for key in members_list:
                    dict_shop1[key] = members[n]
                    n += 1

        except ObjectDoesNotExist:
            print('店舗詳細情報なし')
            dict_shop1 = {}
            dict_shop1['data'] = False #詳細データが取得できなかった時のフラグ
        
        for key in dict_shop1:
            if dict_shop1[key] is not str:
                if dict_shop1[key] is None:
                    dict_shop1[key] = "入力なし"
                dict_shop1[key] = str(dict_shop1[key]) #文字列でないTrueやNoneの場合、文字列にして再代入

        data = json.dumps(dict_shop1)
        # print(data)
        return HttpResponse(data, content_type='application/json')
