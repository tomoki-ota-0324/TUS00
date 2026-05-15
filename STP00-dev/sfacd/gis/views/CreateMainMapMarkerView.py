from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponse
from django.views.generic import View
from django.db.models import Q

from sfacd.gis.models import Shop2, CustomerCars
from sfacd.users.models import User
from sfacd.gis.views.Constant import Constant
from sfacd.gis.views.MainMapView import MainMapView
import geojson
import json
from distutils.util import strtobool #文字列から真偽値への変換
import datetime


class CreateMainMapMarkerView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        """
        表示後に発火したイベントで画面範囲内の店舗、顧客マーカーを作成して返す処理
        """
        features = [] #featureを入れる箱
        marker_kind = request.POST['marker_kind']
        # color_kind = request.POST['color_kind']
        customers, shops = self.get_customers(request)

        # q1 = []
        # query1 = []
        # for customer_id in id_list:
        #     q1.append(Q(id=customer_id))

        # if len(q1) != 0:
        #     query1 = q1.pop()
        #     for item in q1:
        #         query1 |= item
        # customers = Customer.objects.filter(query1)

        for index, customer in enumerate(customers):
            # obj = getattr(customer, marker_kind)
            # if marker_kind == 'sale_flg' and obj is True:
            #     obj = '新'
            # elif marker_kind == 'sale_flg' and obj is None:
            #     obj = '中'
            # elif obj is None:
            #     obj = ' '
            # elif type(obj) is not str:
            #     obj = getattr(obj, marker_kind)
            # else:
            #     obj = ' '
            marker_text = index + 1
            color = "red"
            if marker_kind == "2": #車両層
                if customer.rank.id == 1:
                    color = "pink"
                elif customer.rank.id == 2:
                    color = "orange"
                elif customer.rank.id == 3:
                    color = "green"
            feature = self.create_customer_feature(customer, str(marker_text), color=color)#顧客のpoint feature
            features.append(feature)

        for shop in shops:
            feature = self.create_shop_feature(shop)#店舗のpoint feature
            features.append(feature)

        feature_collection = geojson.FeatureCollection(features)
        print(feature_collection)
        data = json.dumps(feature_collection)
        # print(data)
        return HttpResponse(data, content_type='application/json')
        
    
    def create_customer_feature(self, marker_object, label_text, color='red', stroke='red', zindex_num=1):
        """
        marker_obj: marker model instance
        label_text:マーカーラベルに使うテキスト
        color: マーカーの中の色
        stroke:マーカーの外枠の色
        zindex_num: マーカーの重なり優先度
        """
        lat = marker_object.lat
        lng = marker_object.lng
        customer_id = marker_object.base_customer.id
        if marker_object.rank is None:
            rank = ""
        else:
            rank = marker_object.rank.rank
        name = marker_object.base_customer.name
        address = marker_object.base_customer.address
        car_name = marker_object.car.name
        inspection_date = marker_object.inspection_date
        if inspection_date is None:
            inspection_date = ""
        else:
            inspection_date = inspection_date.strftime('%Y/%m/%d')
        if marker_object.sale_flg:
            sale_flg = "新車"
        else:
            sale_flg = "中古車"
        car_id = marker_object.car.id
        shop_name = marker_object.shop.name
        user_name = marker_object.user.name
        point = geojson.Point((float(lat), float(lng)))
        feature = geojson.Feature(geometry=point, 
            properties={"id": customer_id, "name": name, "rank": rank, "address": address, "car_name": car_name,
                "inspection_date": inspection_date, "sale_flg": sale_flg, "car_id": car_id, "shop_name": shop_name, "user_name": user_name,
                "type": "point", "size": "8", "kind": "customer", "legend_name": label_text, "color": color, "stroke": stroke, "zindex_num": zindex_num})
        return feature

    def create_shop_feature(self, marker_object):
        """
        marker_obj: marker model instance
        label_text:マーカーラベルに使うテキスト
        """
        lat = marker_object.lat
        lng = marker_object.lng
        name = marker_object.name
        point = geojson.Point((float(lat), float(lng)))
        feature = geojson.Feature(geometry=point, properties={"id": marker_object.id, "name": name, "type": "point", "size": "30", "kind": "shop", "legend_name": "店舗"})
        return feature

    def get_customers(self, request):
        """
        デフォルトか検索条件を判定して車両軸顧客を返す
        """
        refine_flg = request.POST['refine_flg'] #検索条件があるかどうか
        top_lat = request.POST['top_lat']
        bottom_lat = request.POST['bottom_lat']
        top_lng = request.POST['top_lng']
        bottom_lng = request.POST['bottom_lng']

        if strtobool(refine_flg): #もし検索条件が設定されているなら
            print('検索の設定あり')
            customers = MainMapView().post(request)
            customers = customers.filter(lat__lte=float(top_lat), lat__gte=float(bottom_lat), lng__lte=float(top_lng), lng__gte=float(bottom_lng)).order_by('id')
            print(customers)
            print(len(customers))
        else:
            print('検索条件なし、デフォルト')
            #ログインユーザー担当の顧客でかつ、現在見ている範囲の中にいる顧客
            customers = CustomerCars.objects.filter(user_id=request.user.id, lat__lte=float(top_lat), lat__gte=float(bottom_lat), lng__lte=float(top_lng), lng__gte=float(bottom_lng)).select_related().order_by('id')
        
        shops = Shop2.objects.filter(lat__lte=float(top_lat), lat__gte=float(bottom_lat), lng__lte=float(top_lng), lng__gte=float(bottom_lng), shop_flg=True)

        return customers, shops
