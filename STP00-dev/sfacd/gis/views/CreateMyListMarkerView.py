from django.views.generic import View
from django.db.models import Q
from django.http.response import HttpResponse

from sfacd.gis.models import Shop, Customer, Mylist
from sfacd.users.models import User
import geojson
import json


class CreateMyListMarkerView(View):
    """
    ajaxで発動して、マイリストのマーカーを作成
    """
    def post(self, request, *args, **kwargs):
        """
        選択されたマイリストに登録されている顧客を表示するためのマーカーを作成する
        """
        features = [] #featureを入れる箱

        mylist_id = request.POST['mylist_id'] #現在選択されているマイリストid
        print("mylist_id:" + mylist_id)
        marker_color = request.POST['marker_color'] #マーカーの色分け基準
        current_user = request.user
        current_shop = Shop.objects.get(id=current_user.shop_id) #ユーザー所属店舗
        mylist = Mylist.objects.get(id=int(mylist_id))
        customers = mylist.customers.all() #マイリストに記載の顧客全て
        lst = list(customers.values_list(marker_color, flat=True).order_by(marker_color).distinct()) #色分け基準カラムの要素のユニークリスト
        for customer in customers:
            feature = self.create_feature(customer, 0, marker_color, lst) #顧客のpoint feature
            features.append(feature)

        feature = self.create_feature(current_shop, 1, marker_color, lst) #店舗のpoint feature
        features.append(feature)

        feature_collection = geojson.FeatureCollection(features)
        print(feature_collection)
        data = json.dumps(feature_collection)
        # print(data)
        return HttpResponse(data, content_type='application/json')
        
    
    def create_feature(self, marker_object, recode_type, marker_type, lst):
        """
        marker_obj: marker model instance
        recode_type: 0: customer, 1: shop
        marker_type: rank_kind, car_typeなどのカラム名 
        lst: marker_typeのuniqe要素が入ったリスト
        """

        if recode_type == 0: #顧客マーカー
            legend_name = getattr(marker_object, marker_type)
            image_path = str(lst.index(legend_name)) + ".png"
            lat = marker_object.lat
            lng = marker_object.lng
            address = marker_object.address
            point = geojson.Point((float(lat), float(lng)))
            feature = geojson.Feature(geometry=point, properties={"name": address, "type": "point", "marker": image_path, "size": "10", "kind": "customer", "legend_name": legend_name})
        elif recode_type == 1: #店舗マーカー
            image_path = 'toyota2.png'
            lat = marker_object.lat
            lng = marker_object.lng
            name = marker_object.name
            point = geojson.Point((float(lat), float(lng)))
            feature = geojson.Feature(geometry=point, properties={"name": name, "type": "point", "marker": image_path, "size": "30", "kind": "shop", "legend_name": "店舗"})

        return feature
