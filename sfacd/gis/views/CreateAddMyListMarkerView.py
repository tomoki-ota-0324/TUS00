from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponse
from django.views.generic import View
from django.db.models import Q

from sfacd.gis.models import Shop2, CustomerCars, Mylist2
from sfacd.users.models import User
from sfacd.gis.views.Constant import Constant
from sfacd.gis.views.CreateMainMapMarkerView import CreateMainMapMarkerView
import geojson
import json
from distutils.util import strtobool #文字列から真偽値への変換
import datetime


class CreateAddMyListMarkerView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        """
        既存のマーカーに選択したマイリストマーカーを追加で作成する
        """
        # 仮設置
        mylist_id = 1

        current_mylist = Mylist2.objects.get(id=mylist_id)
        customers = current_mylist.customer_cars.all()
        print(customers)

        features = [] #featureを入れる箱
        marker_kind = request.POST['marker_kind']

        for customer in customers:
            obj = getattr(customer, marker_kind)
            if marker_kind == 'sale_flg' and obj is True:
                obj = '新'
            elif marker_kind == 'sale_flg' and obj is None:
                obj = '中'
            elif obj is None:
                obj = ' '
            elif type(obj) is not str:
                obj = getattr(obj, marker_kind)
            else:
                obj = ' '
            feature = CreateMainMapMarkerView().create_customer_feature(customer, obj, stroke="blue", zindex_num=3)#顧客のpoint feature
            features.append(feature)

        feature_collection = geojson.FeatureCollection(features)
        print(feature_collection)
        data = json.dumps(feature_collection)
        # print(data)
        return HttpResponse(data, content_type='application/json')
