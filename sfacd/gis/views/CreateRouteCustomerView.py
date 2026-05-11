from django.views.generic import View
from django.db.models import Q
from django.http.response import HttpResponse

from sfacd.gis.models import Shop, Customer, Mylist
from sfacd.users.models import User
import geojson
import json


class CreateRouteCustomerView(View):
    """
    旧アタックリスト進捗画面のメイン訪問先マーカー作成機能
    """
    def post(self, request, *args, **kwargs):
        """
        旧アタックリスト表示機能のメインで選択されている訪問箇所のマーカーgeojsonを作って返す処理
        """
        features = [] #featureを入れる箱

        id_list = request.POST.getlist('id_list[]') #現在選択されているメイン訪問箇所
        q1 = []
        query1 = []
        for customer_id in id_list:
            q1.append(Q(id=customer_id))

        if len(q1) != 0:
            query1 = q1.pop()
            for item in q1:
                query1 |= item
        customers = Customer.objects.filter(query1)

        for index, customer in enumerate(customers):
            feature = self.create_feature(customer, index)#顧客のpoint feature
            features.append(feature)

        feature_collection = geojson.FeatureCollection(features)
        print(feature_collection)
        data = json.dumps(feature_collection)
        # print(data)
        return HttpResponse(data, content_type='application/json')
        
    
    def create_feature(self, marker_object, label_text):
        """
        marker_obj: marker model instance
        label_text:マーカーラベルに使うテキスト
        """
        lat = marker_object.lat
        lng = marker_object.lng
        address = marker_object.address
        point = geojson.Point((float(lat), float(lng)))
        feature = geojson.Feature(geometry=point, properties={"name": address, "type": "point", "size": "10", "kind": "customer", "legend_name": label_text})

        return feature
