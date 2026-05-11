from django.views.generic import View
from django.db.models import Q
from django.http.response import HttpResponse

from sfacd.gis.models import Shop2, GisCustomer, Rank
from sfacd.users.models import User
from sfacd.gis.views.Constant import Constant
import geojson
import json
import os
import random
import time


class CreateCustomerMarkerView(View):
    # mark_list = {} #凡例：{X:Y},
    mark_list = {}
    max_marker_icon = Constant().max_marker_icon_num

    def post(self, request, *args, **kwargs):
        """
        商圏分析の作成マーカーを絞込み、geojson形式で返す
        """
        self.mark_list = {}  # リセット
        # print("マーカー絞込")

        features = []  # featureを入れる箱

        shop_ids = request.POST.getlist('shops[]')
        user_ids = request.POST.getlist('users[]')
        show_shop = request.POST.getlist('show_shop[]')
        sale_flg = request.POST.getlist('sale_flg[]')
        sex = request.POST.getlist('sex[]')
        customer_fixed_kind = request.POST.getlist('customer_fixed_kind[]')
        car_fixed_kind = request.POST.getlist('car_fixed_kind[]')
        customer_rank = request.POST.getlist('giscustomer_customer_rank[]')
        car_rank = request.POST.getlist('giscustomer_cars_rank[]')
        marker_color = request.POST['marker_color']
        car_model = request.POST['car_model']
        service_shop_ids = request.POST.getlist('service_shops[]')
        default_marker = request.POST['default_marker']

        if default_marker == 'false':  # デフォルト表示時でない場合
            # print("通常顧客絞込")
            customers = GisCustomer.objects.all().exclude(lat=None, lng=None)  # ジオコーディングができているもののみ
            # customers = GisCustomer.objects.filter(location_rank=4) #正確性4のGeocodingのみ表示
            # customers = GisCustomer.objects.filter(location_rank=4, shop__shop_flg=True) #正確性4かつ実店舗顧客のみ
            customers = customers.filter(shop__shop_flg=True)  # GeoCordingが成功した実店舗の全顧客表示
            # print(len(customers))
            car_model = car_model.strip()  # 前後空白の削除
            if car_model != "":  # もし型式が入力されていたら
                customers = customers.filter(car_model__icontains=car_model)  # 大文字小文字区別なし部分一致
                # customers = customers.filter(car_model__istartswith=car_model) #大文字小文字区別なし前方一致

            if len(shop_ids) > 0:
                q1 = []
                query1 = []
                for shop_id in shop_ids:
                    q1.append(Q(shop_id=shop_id))

                if len(q1) != 0:
                    query1 = q1.pop()
                    for item in q1:
                        query1 |= item  # 選択店舗での絞り込み
                customers = customers.filter(query1)

            # print(len(customers))
            if len(user_ids) > 0:
                q1 = []
                query1 = []
                for user_id in user_ids:
                    q1.append(Q(user_id=user_id))

                if len(q1) != 0:
                    query1 = q1.pop()
                    for item in q1:
                        query1 |= item  # 選択スタッフでの絞り込み
                customers = customers.filter(query1)

            # print(len(customers))
            if len(sex) > 0:
                q1 = []
                query1 = []
                for sex_num in sex:
                    if sex_num == '':
                        sex_num = None
                    q1.append(Q(sex=sex_num))

                if len(q1) != 0:
                    query1 = q1.pop()
                    for item in q1:
                        query1 |= item  # 性別での絞り込み
                customers = customers.filter(query1)

            # print(len(customers))
            if len(customer_fixed_kind) > 0:
                q1 = []
                query1 = []
                for fixed_kind in customer_fixed_kind:
                    if fixed_kind == '':
                        fixed_kind = None
                    q1.append(Q(customer_fixed_kind=fixed_kind))

                if len(q1) != 0:
                    query1 = q1.pop()
                    for item in q1:
                        query1 |= item  # 顧客固定客での絞り込み
                customers = customers.filter(query1)

            # print(len(customers))
            if len(customer_rank) > 0:
                q1 = []
                query1 = []
                for rank_id in customer_rank:
                    q1.append(Q(customer_rank_id=rank_id))

                if len(q1) != 0:
                    query1 = q1.pop()
                    for item in q1:
                        query1 |= item  # 顧客層別での絞り込み
                customers = customers.filter(query1)

            # print(len(customers))
            if len(car_fixed_kind) > 0:
                q1 = []
                query1 = []
                for fixed_kind in car_fixed_kind:
                    if fixed_kind == '':
                        fixed_kind = None
                    q1.append(Q(car_fixed_kind=fixed_kind))

                if len(q1) != 0:
                    query1 = q1.pop()
                    for item in q1:
                        query1 |= item  # 車両固定客での絞り込み
                customers = customers.filter(query1)

            # print(len(customers))
            if len(car_rank) > 0:
                q1 = []
                query1 = []
                for rank_id in car_rank:
                    q1.append(Q(car_rank_id=rank_id))

                if len(q1) != 0:
                    query1 = q1.pop()
                    for item in q1:
                        query1 |= item  # 車両層別での絞り込み
                customers = customers.filter(query1)

            if len(sale_flg) > 0:
                q1 = []
                query1 = []
                for flg in sale_flg:
                    if flg == '0':
                        flg = None
                    q1.append(Q(sale_flg=flg))

                if len(q1) != 0:
                    query1 = q1.pop()
                    for item in q1:
                        query1 |= item  # 販売区分での絞り込み
                customers = customers.filter(query1)

            if len(service_shop_ids) > 0:
                q1 = []
                query1 = []
                for shop_id in service_shop_ids:
                    q1.append(Q(service_shop_id=shop_id))

                if len(q1) != 0:
                    query1 = q1.pop()
                    for item in q1:
                        query1 |= item  # 選択店舗での絞り込み
                customers = customers.filter(query1)

            # print(len(customers))
            # print(customers.query)
            # customers = customers.order_by(marker_color)

            customers = customers.order_by('lat')  # まず緯度でソート
            compare_lat = 0  # 比較対象緯度
            compare_lng = 0  # 比較対象経度
            num_lat = 0  # 積み上げ緯度
            save_dic = {}  # {id: float_lat}
            # before_time = time.time()
            for customer in customers:  # 緯度順にソートされている
                if compare_lat == customer.lat and compare_lng == customer.lng and customer.lat is not None and customer.lng is not None:  # もし緯度経度が前のインスタンスと同じでかつ、緯度経度がNoneでない場合
                    # print("一緒！！！！！" + str(num_lat))
                    num_lat += 0.00001
                    save_dic[customer.id] = customer.lat + num_lat  # idをキーとしてインスタンス緯度と積み上げ緯度を足したものをvalueに入れる
                else:
                    # print("違う！！！！！！" + str(num_diff))
                    compare_lat = customer.lat  # 比較緯度の変更
                    compare_lng = customer.lng  # 比較経度の変更
                    num_lat = 0  # 緯度積み上げのリセット
            # print(save_dic)
            # print('重複通過')
            # print(time.time() - before_time)
            # before_time = time.time()
            customers = customers.select_related('shop', 'user', 'customer_rank', 'car_rank', 'service_shop').order_by(
                marker_color)  # マーカーカラー選択されたものでソートし直し
            for customer in customers:
                feature = self.create_feature(customer, 1, marker_color, save_dic)  # ここが遅い
                features.append(feature)  # 顧客マーカーを作成した
            # print('カスタマー通過')
            # print(time.time() - before_time)
        else:
            # print('初期画面表示、店舗マーカーのみ')
            print('初期表示')

        # shops = Shop2.objects.filter(shop_flg=True) #全実店舗
        # if len(show_shop) > 0: #一つ以上の選択がある場合
        #     q1 = []
        #     query1 = []
        #     q2 = []
        #     query2 = []
        #     if not '0' in show_shop: #もしレクサスが選択されていなかったら
        #         shops = shops.filter(brand_id=14601) #レクサス以外に絞る

        #     if '1' in show_shop or '2' in show_shop: #もし新車店か中古車店が選択されていたら
        #         for flg in show_shop:
        #             if flg == '1': #新車店舗示
        #                 q1.append(Q(new_flg=True))
        #             elif flg == '2': #中古車店舗表示
        #                 q1.append(Q(ucar_flg=True))
        #             else:
        #                 continue #0の場合スルー

        #         if len(q1) != 0:
        #             query1 = q1.pop()
        #             for item in q1:
        #                 query1 |= item #店舗表示での絞り込み
        #         shops = shops.filter(query1)
        #     elif '0' in show_shop and not '1' in show_shop and not '2' in show_shop: #レクサスが選択されていて、新車、中古車が選択されていない場合
        #     # elif '0' in show_shop and '3' in show_shop and not '1' in show_shop and not '2' in show_shop or len(show_shop) == 1 and show_shop[0] == '0': #LEXUS店舗とトヨペットのみが選ばれている場合、もしくはLEXUS店舗のみが選ばれている場合
        #         shops = shops.exclude(brand_id=14601) #レクサスのみに絞る
        #     if '3' in show_shop or '4' in show_shop or '5' in show_shop or '6' in show_shop: #もし、トヨペット、カローラ、ネッツ、候補地のチェックが選択されていたら
        #         for flg in show_shop:
        #             if flg == '3': #トヨペット
        #                 q2.append(Q(shop_kind=1))
        #             elif flg == '4': #カローラ
        #                 q2.append(Q(shop_kind=2))
        #             elif flg == '5': #ネッツ
        #                 q2.append(Q(shop_kind=3))
        #             elif flg == '6': #候補地
        #                 q2.append(Q(shop_kind=4))
        #             else:
        #                 continue #0の場合スルー

        #         if len(q2) != 0:
        #             query2 = q2.pop()
        #             for item in q2:
        #                 query2 |= item #店舗表示での絞り込み
        #         shops = shops.filter(query2)

        # print(len(shops))
        # shops = shops.order_by('shop_kind', 'id') #店舗系列でソートした中の、IDの順序
        # print(shops)

        shops = Shop2.objects.filter(shop_flg=True, id__in=show_shop).order_by('shop_kind', 'id')

        if len(show_shop) > 0:  # 店舗表示チェックが入ってなかったらfeatureに入れない
            for shop in shops:
                feature = self.create_feature(shop, 0, marker_color)  # 店舗全体のアイコン使用 ここが遅い
                features.append(feature)  # 店舗マーカーを作成した

        # print("顧客マーカー＋店舗：{}".format(len(customers) + len(shops))) #チェック用
        # self.count_color_marker(customers, marker_color) #属性ごとの数をプリント　チェック用
        feature_collection = geojson.FeatureCollection(features)
        # print(feature_collection)
        data = json.dumps(feature_collection)
        # print(data)
        return HttpResponse(data, content_type='application/json')

    def create_feature(self, obj, marker_type, marker_color, save_dic={}):
        """
        店舗マーカーと顧客マーカーのfeatureを作成
        obj: customer or shop
        marker_type: int 0: create shop marker, 1:create customer marker
        marker_color: select marker_color
        save_dic: {customer.id: lat}
        """

        if obj.lat is None or obj.lng is None:  # 住所の登録がない顧客ははじく
            feature = None
        else:
            if marker_type == 0:  # 店舗マーカー作成
                # image_path = 'toyota2.png'
                image_info_dict = self.get_shop_marker_filename(obj.shop_kind)  # トヨペット系、カローラ、ネッツ、候補地のマーカー画像を選択
                image_path = image_info_dict['image']  # 画像ファイル名
                legend_name = image_info_dict['shop_name']  # 店舗系列名
                lat = obj.lat
                lng = obj.lng
                name = obj.name
                shop_id = obj.id
                point = geojson.Point((float(lat), float(lng)))
                # STT KINTO ADD&MOD 20190619
                keiretsu = obj.shop_kind
                feature = geojson.Feature(geometry=point, properties={
                    "name": name, "type": "point", "marker": image_path, "size": "35", "kind": "shop", "legend_name": legend_name, "shop_id": shop_id, "keiretsu": keiretsu,
                })
                # END KINTO MOD 20190619
            elif marker_type == 1:  # 顧客マーカー作成
                legend_name = getattr(obj, marker_color)
                if type(legend_name) != str:
                    legend_name = legend_name.__str__()
                # color = self.get_marker_color(legend_name) #scc sprite imageを使用時に使用
                image_path = self.get_image_path(legend_name)  # 画像一つ一つ表示時に使用
                if obj.id in save_dic.keys():
                    lat = save_dic[obj.id]
                else:
                    lat = obj.lat
                lng = obj.lng
                # address = obj.google_address
                if obj.customer_rank is None:
                    customer_rank = "入力なし"
                else:
                    customer_rank = obj.customer_rank.rank
                if obj.car_rank is None:
                    car_rank = "入力なし"
                else:
                    car_rank = obj.car_rank.rank
                if obj.car_model is None:
                    car_model = "入力なし"
                else:
                    car_model = obj.car_model
                if obj.car_name is None:
                    car_name = "入力なし"
                else:
                    car_name = obj.car_name
                # label = "顧客層：" + customer_rank + ", 車両層：" + car_rank + ", 型式：" + car_model + ", 車両名：" + car_name + ", 番号：" + obj.car_num + ", 緯度経度：" + str(lat) + ", " + str(lng) #デバッグ用
                label = "顧客層：" + customer_rank + ", 車両層：" + car_rank + ", 型式：" + car_model + ", 車両名：" + car_name
                point = geojson.Point((float(lat), float(lng)))
                feature = geojson.Feature(geometry=point, properties={
                    "name": label, "type": "point", "marker": 'g' + image_path, "size": "10", "kind": "customer", "legend_name": legend_name,
                })
                # 以下CSS Spriteで使用
                # feature = geojson.Feature(geometry=point, properties={
                #     "name": address, "type": "point", "size": "340", "kind": "customer", "legend_name": legend_name, "x": color['x'], "y": color['y'],
                #     })
        return feature

    def get_image_path(self, legend_name):
        """
        画像一つ一つ選択表示するマーカーを作成する場合
        """
        if legend_name in self.mark_list:
            image_path = self.mark_list[legend_name]
        else:
            if self.max_marker_icon <= len(self.mark_list):  # マーカーアイコンが用意しているマーカー数より多い場合
                index = len(self.mark_list) + 1
                # print("最大数より大きい場合")
                image_path = str(index % self.max_marker_icon) + ".png"
                self.mark_list[legend_name] = image_path
            else:
                index = len(self.mark_list) + 1
                image_path = str(index) + ".png"
                self.mark_list[legend_name] = image_path
                # print(image_path)
        return image_path

    def get_marker_color(self, legend_name):
        """
        1枚の画像でCSS Spriteを利用し表示する場合
        return color: {X, Y}
        legend_name: str
        """
        base_num = 30  # 各アイコンの幅、画像間隔、ピクセル
        if legend_name in self.mark_list:  # 辞書に凡例名のキーが既に入っていた場合
            color = self.mark_list[legend_name]
        else:  # 辞書に凡例名キーがまだなかった場合
            x = 0
            index = len(self.mark_list)
            if index == 0:
                y = 0
            elif index > 0:
                num = index % 7
                y = base_num * num

            if index > 6:
                num = index // 6 - 1
                x = base_num * num
            self.mark_list[legend_name] = {"x": x, "y": y}
            color = {"x": x, "y": y}
        return color

    def count_color_marker(self, customers, marker_color):
        """
        デバッグ用
        マーカーを色別にカウントする
        """
        base = None
        flg = False
        lst = []
        for customer in customers:
            if base is None:
                flg = True
            elif base == getattr(customer, marker_color):
                flg = False
            elif base in lst:
                flg = False
            else:
                flg = True

            if flg:
                base = getattr(customer, marker_color)
                if marker_color == 'shop':
                    shops = Shop2.objects.all()
                    for shop in shops:
                        print(shop.name + " :{}".format(len(customers.filter(shop_id=shop.id))))
                elif marker_color == 'customer_rank':
                    ranks = Rank.objects.all()
                    for rank in ranks:
                        print(rank.rank + " :{}".format(len(customers.filter(customer_rank_id=rank.id))))
                elif marker_color == 'car_rank':
                    ranks = Rank.objects.all()
                    for rank in ranks:
                        print(rank.rank + " :{}".format(len(customers.filter(car_rank_id=rank.id))))
                elif marker_color == 'sale_flg':
                    flg_list = [1, 2, 9]
                    for flg in flg_list:
                        print(str(flg) + " :{}".format(len(customers.filter(sale_flg=flg))))
                flg = False
                lst.append(base)
            else:
                continue

    def get_shop_marker_filename(self, num):
        """
        マーカーアイコン画像ファイル名と、その凡例名を返す
        num: shop_kind
        image: image file name
        shop_name: shop type name
        return {image: image, shop_name: shop_name}, ex: {image: "toyopet.png", shop_name: "静岡トヨペット"}
        """
        if num == 1:  # トヨペット店舗画像 22/11/2 統合により変更 => トヨタユナイテッド静岡
            # return {'image': 'toyopet.png', 'shop_name': '静岡トヨペット'}
            return {'image': 'toyopet.png', 'shop_name': 'トヨタユナイテッド静岡'}
        elif num == 2:  # カローラ東海画像
            return {'image': 'corolla.png', 'shop_name': 'カローラ東海'} # 統合により現在利用なし(22/11/2)
        elif num == 3:  # ネッツスルガ画像
            return {'image': 'netz.png', 'shop_name': 'ネッツスルガ'} # 統合により現在利用なし(22/11/2)
        elif num == 4:  # 候補地画像
            return {'image': 'star.png', 'shop_name': '候補地点'}
        else:  # その他　入力ミスなど
            return {'image': 'toyota2.png', 'shop_name': 'その他'}
