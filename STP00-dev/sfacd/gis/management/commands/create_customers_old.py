from django.core.management import BaseCommand
from django.db.models import Q

from sfacd.gis.models import Car, Shop2, GisCustomer
from sfacd.users.models import User
from sfacd.gis.views.Constant import Constant

import time
import csv
import datetime
import pandas
import numpy
import googlemaps
# from mojimoji import han_to_zen, zen_to_han #車名半角カタカナを直す必要があれば実施

class Command(BaseCommand):
    """
    カスタムコマンド
    """   
    help = '自動差分顧客情報取込みコマンド'
    #定数
    input_file_path = Constant().input_file_path #仮設置パス
    output_file_path = Constant().output_file_path
    only_read_columns = {'お客様コード': 'object', '性別区分': 'int64', '郵便番号': 'object', 'お客様住所漢字': 'object', '顧客固定客区分': 'int64', '顧客層別区分': 'int64', '登録ＮＯ.': 'object', '型式': 'object',
        '車名': 'object', '新中区分': 'int64', '軽区分': 'int64', '業直区分': 'int64', '車両固定客区分': 'int64', '車両層別区分': 'int64', '担当スタッフコード': 'int64',
        '担当スタッフ名': 'object', '担当店舗コード': 'int64', '担当店舗名': 'object', 'サービス店舗コード': 'int64', 'サービス店舗名': 'object'}
    #google map client
    gmaps = googlemaps.Client(key=Constant().SERVER_API) #デフォルトでGoogleとHTTPS接続 https://github.com/googlemaps/google-maps-services-python/blob/master/googlemaps/client.py
    text_list = [] #処理結果をテキストファイルに出力するときに使用

    def add_arguments(self, parser): #コマンドのオプションを設定できる。引数を必要としない場合は、この関数の実装は必須ではない
        parser.add_argument('--update', help='一度取り込んだCSVのマスタデータ登録後の更新登録', action="store_true") #デフォルトは差分の取込み py manage.py create_customers --update

    def handle(self, *args, **kwargs):
        """
        CSVより自動顧客情報取込み機能
        optionのない場合：車両軸データCSVにあるデータをすべて新規レコードとして登録する。そのレコードにマスタデータにない新規車両があれば、追加登録する。
            また新規店舗、新規社員番号が見つかれば、それをテキストで出力し、知らせる。新規店舗には住所、緯度経度、新規社員にはe-mailなどが必要なため、自動登録はされない。

        --update option ：オプションなしで一度登録したCSVデータからマスタデータがなくてNoneで一時登録したデータを、マスタデータ登録後に内容を更新する。
        """
        try:
            print("注意：本番環境ではダンプファイルを作成してから実施する")
            before_time = time.time() #処理前の時刻
            before_customer_query = GisCustomer.objects.all() #処理前の車両顧客インスタンス
            rank4_len = len(GisCustomer.objects.exclude(location_rank=4)) #処理前のgeocoding_rank4以外の件数
            partial_len = len(GisCustomer.objects.filter(partial_match=True)) #処理前の部分一致処理件数
            text = "処理開始：{}".format(datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
            print(text)
            self.text_list.append(text)
            data = self.read_csv() #CSVからの読込と文字列正規化
            text = "読込データ行数：{}行".format(str(len(data)))
            print(text)
            self.text_list.append(text)
            print("読み込んだCSVを加工前にコピーを取っておくかどうか")
            today = datetime.datetime.today()
            st_today = today.strftime('%Y-%m-%d')
            self.create_csv(data, st_today + '_read.csv') ##加工前（データの空文字処理のみ）に読み込んだデータを吐き出す
            data = self.check_master_table(data) #リレーションテーブルの確認とデータの正規化
            customers = self.create_customer(data, update=kwargs['update']) #緯度経度以外の一時保存
            if kwargs['update']: #True
                text = "更新されたデータ件数：{}件".format(str(len(customers)))
                print(text)
                self.text_list.append(text)
                text = "処理が完了しました。経過時間：{}秒".format(time.time() - before_time)
                self.text_list.append(text)
                print(text)
            else:
                text = "緯度経度出力前保存件数：{}件".format(str(len(customers)))
                print(text)
                self.text_list.append(text)
                add_latlng_customers = self.geocoding(customers) #一時登録インスタンスの緯度経度保存処理 returnはList型
                text = "緯度経度出力保存件数：{}件".format(str(len(add_latlng_customers)))
                print(text)
                self.text_list.append(text)
                query_customers = GisCustomer.objects.exclude(location_rank=4)
                text = "今回登録されたレベル4未満Geocoding件数：{}件".format(str(len(query_customers) - rank4_len))
                print(text)
                self.text_list.append(text)
                query_customers = GisCustomer.objects.filter(partial_match=True)
                text = "今回登録された部分一致住所取得件数：{}件".format(str(len(query_customers) - partial_len))
                print(text)
                self.text_list.append(text)
                text = "処理が完了しました。経過時間：{}秒、緯度経度変換できない件数：{}件".format(time.time() - before_time, len(customers) - len(add_latlng_customers))
                self.text_list.append(text)
                print(text)
        except Exception as e:
            text = 'ExceptionError 発生：{}'.format(e)
            print(text)
            self.text_list.append(text)
        finally:
            self.write_txt(st_today + '_result.txt')

    def read_csv(self, *args, **kwargs):
        """
        CSV読込と文字列正規化処理
        """
        text = "CSV読込開始"
        print(text)
        self.text_list.append(text)
        columns_list = list(self.only_read_columns.keys())
        data = pandas.read_csv(self.input_file_path, encoding="CP932", usecols=columns_list, dtype='object', na_filter=False) #空、空白を欠損値(NaN)として扱わない
        # print(data['お客様住所漢字'])
        check_columns = list(data.columns) #現在のcolumns（ヘッダー）のみ

        for row in check_columns:
            if data[row].dtype == 'object':
                data[row] = data[row].str.strip() #文字列前後に存在する空白を除去
                data[row].str.replace('\u3000', '') #文字列中間に存在する空白を除去
            if self.only_read_columns[row] == 'int64': #もしInt型にしたいカラムなら
                for index, value in enumerate(data[row]): #リストを展開して
                    if value == '': #要素が空なら
                        data.loc[index, row] = None # Noneを代入する
        # data = data.astype(self.only_read_columns) #型変換
        return data

    def create_customer(self, data, *args, **kwargs):
        """
        顧客のインスタンス作成、緯度経度以外の保存処理
        """
        text = "顧客情報の一時登録func開始"
        print(text)
        self.text_list.append(text)
        _instances = [] #作成したインスタンスを入れるリスト
        if kwargs['update']: #True
            text = "UPDATE登録処理" #ここでの扱い方どうするか
            print(text)
            self.text_list.append(text)
            for index, row in data.iterrows():
                customers = GisCustomer.objects.filter(customer_code=row[0], car_num=row[6]).filter(Q(shop_id=None)|Q(user_id=None)|Q(service_shop_id=None))
                if len(customers) > 1:
                    text = '同一更新レコード{}件あり'.format(len(customers))
                    print(text)
                    self.text_list.append(text)
                    ids = ""
                    for customer in customers:
                        ids += (str(customer.id) + ', ')
                    text = 'レコードを手動で変更してください。\ngiscustomer_id：{},\nユーザーID：{},\n担当店舗ID：{},\nサービス店舗ID：{}'.format(ids, row[13], row[15], row[17])
                    print(text)
                    self.text_list.append(text)
                elif len(customers) == 1:
                    customer = customers[0]
                    "更新レコード：{}".format(customer)
                    customer.shop_id = row[16] #担当店舗コード　固定値注意
                    customer.user_id = row[14] #担当者コード
                    customer.service_shop_id = row[18] #サービス店舗コード
                    _instances.append(customer)
                else:
                    continue
            self.save(_instances)
            return _instances
        else:
            text = "通常登録処理"
            print(text)
            self.text_list.append(text)
            for index, row in data.iterrows():
                # print(index)
                # print(row)
                # print(row[1])
                customer = GisCustomer(customer_code=row[0], sex=row[1], post_code=row[2], address=row[3], customer_fixed_kind=row[4], customer_rank_id=row[5], car_num=row[6], sale_flg=row[9], mini_flg=row[10],
                    direct_kind=row[11], car_fixed_kind=row[12], car_rank_id=row[13], service_shop_id=row[18], car_id=row[7], shop_id=row[16], user_id=row[14]) #インスタンスの作成 固定値注意
                _instances.append(customer)
            self.save(_instances) #ここで保存
            return _instances
            
    def check_master_table(self, data, *args, **kwargs):
        """
        登録データとリレーションでつながるマスタデータがあるか確認し、なければ作成、保存
        """
        text = "マスターテーブルとのリレーション整合性確認"
        print(text)
        self.text_list.append(text)
        cars = Car.objects.values_list('id', flat=True) #IDのみのクエリセット
        users = User.objects.values_list('username', flat=True)
        shops = Shop2.objects.values_list('id', flat=True)
        new_cars = [] #新しく保存が必要な車両インスタンスリスト
        new_users = [] #新しく保存が必要なユーザーインスタンスリスト
        new_shops = [] #新しく保存が必要な店舗インスタンスリスト
        new_service_shops = [] #新しく保存が必要なサービス店舗インスタンスリスト
        #-------------------------------車両チェック------------------------------------
        for index, car in enumerate(data['型式']):
            if car != '' and not car in cars: #もし車型が空でなく、車両テーブルに車両がない場合
                print('車両登録')
                new_car = Car(id=car, name=data['車名'][index]) #車両インスタンスの作成
                new_cars.append(new_car)
        if len(new_cars) > 0:
            self.save(new_cars) #車両インスタンスの登録
            text = "新しく登録した車両数：{}".format(len(new_cars))
            print(text)
            self.text_list.append(text)
        #-------------------------------ユーザーチェック----------------------------------
        for index, user in enumerate(data['担当スタッフコード']):
            if user is not None and not user in users: #もしユーザーカラムにデータがあり、ユーザーIDの登録がされてない場合
                print('ユーザー登録')
                new_users.append({'id': user, 'name': data['担当スタッフ名'][index], 'index': index})
        if len(new_users) > 0:
            text = "ユーザー登録が先に必要な車両レコードが、{}件あります。ユーザーリレーションをNoneとして登録します。".format(len(new_users))
            print(text)
            self.text_list.append(text)
            for user in new_users:
                text = "ユーザー [id: {}, name: {}]、\n対象車両レコード: {}".format(user['id'], user['name'], data.iloc[user['index']])
                print(text)
                self.text_list.append(text)
                data.loc[user['index'], '担当スタッフコード'] = None #仮登録措置
        #---------------------------------担当店舗チェック---------------------------------
        for index, shop in enumerate(data['担当店舗コード']):
            if shop is not None and not int(shop) in shops: # shopsの中身IDがInt型なので注意
                #店舗登録
                print('店舗登録(担当店舗)')
                new_shops.append({'id': shop, 'name': data['担当店舗名'][index], 'index': index})
        if len(new_shops) > 0:
            text = "店舗登録が先に必要な車両レコードが、{}件あります。担当店舗リレーションをNoneとして登録します。".format(len(new_shops))
            print(text)
            self.text_list.append(text)
            for shop in new_shops:
                text = "店舗 [id: {}, name: {}]、\n対象車両レコード: {}".format(shop['id'], shop['name'], data.iloc[shop['index']])
                print(text)
                self.text_list.append(text)
                data.loc[shop['index'], '担当店舗コード'] = None #仮登録措置
        #--------------------------------サービス店舗チェック-------------------------------
        for index, service_shop in enumerate(data['サービス店舗コード']):
            if service_shop is not None and not int(service_shop) in shops:
                #店舗登録
                print('店舗登録(サービス店舗)')
                new_service_shops.append({'id': service_shop, 'name': data['サービス店舗名'][index], 'index': index})
        if len(new_service_shops) > 0:
            text = "店舗登録が先に必要な車両レコードが、{}件あります。サービス店舗リレーションをNoneとして登録します。".format(len(new_service_shops))
            print(text)
            self.text_list.append(text)
            for service_shop in new_service_shops:
                text = "店舗 [id: {}, name: {}]、\n対象車両レコード: {}".format(service_shop['id'], service_shop['name'], data.iloc[service_shop['index']])
                print(text)
                self.text_list.append(text)
                data.loc[service_shop['index'], 'サービス店舗コード'] = None #仮登録措置

        return data

    def geocoding(self, customers, *args, **kwargs):
        """
        仮登録されたデータの緯度経度をGeocodingし、取得できれば更新
        """
        
        text = "顧客情報のGeocoding func開始"
        print(text)
        self.text_list.append(text)
        _instances = []
        for customer in customers:
            location = self.get_location(customer.address)
            # print(location)
            lat = location[customer.address]['lat']
            lng = location[customer.address]['lng']
            address = location[customer.address]['address']
            rank = location[customer.address]['location_rank']
            partial_match = location[customer.address]['partial_match']
            if lat == "" or lng == "":
                continue #処理できなかったものはリストに入れず更新しない。そのまま次へ
            else:
                customer.lat = lat
                customer.lng = lng
                customer.google_address = address
                customer.partial_match = partial_match
                if rank == "ROOFTOP":
                    customer.location_rank = 4
                elif rank == "RANGE_INTERPOLATED":
                    customer.location_rank = 3
                elif rank == "GEOMETRIC_CENTER":
                    customer.location_rank = 2
                elif rank == "APPROXIMATE":
                    customer.location_rank = 1
                else:
                    customer.location_rank = None
                _instances.append(customer)
        self.save(_instances) #リスト内のインスタンスの更新処理
        return _instances

    def save(self, _instances):
        """
        インスタンスの保存
        _instances: models instances list
        """
        for obj in _instances:
            obj.save()
        text = "保存完了"
        print(text)
        self.text_list.append(text)

    def get_location(self, text_location):
        '''
        送られてきた場所名を引数に、緯度、経度を、その名前とともに返す
        text_location: String
        return {地名: {lat: lat_num, lng: lng_num}}
        '''
        location_dict = {}
        print(text_location)
        if text_location == "":
            location_dict = {text_location: {"lat": "", "lng": "", "address": "", "location_rank": "", "partial_match": ""}}
        else:
            geo_result = self.gmaps.geocode(address=text_location, language='ja')
            if len(geo_result) == 0:
                location_dict = {text_location: {"lat": "", "lng": "", "address": "", "location_rank": "", "partial_match": ""}}
            else:
                location = geo_result[0]['geometry']['location'] #緯度経度
                location['address'] = geo_result[0]['formatted_address'] #正規化住所
                location['location_rank'] = geo_result[0]['geometry']['location_type'] #出力ランク
                if 'partial_match' in geo_result[0].keys():
                    location['partial_match'] = True #部分一致で返された住所の場合 True
                else:
                    location['partial_match'] = False
                location_dict[text_location] = location
        return location_dict #{検索名: {lat: lat_num, lng: lng_num, address: japanese_address, location_rank: 'ROOFTOP', partial_match: False}}

    def create_csv(self, data, file_name):
        """
        加工前（データの空文字処理のみ）に読み込んだデータを吐き出す
        """
        path = self.output_file_path + file_name
        data.to_csv(path, encoding="CP932")

    def write_txt(self, file_name):
        """
        処理経過を書き出す、特に必要なマスターデータの変更など
        """
        with open(self.output_file_path + file_name, mode="w", encoding="CP932") as f:
            all_text = ""
            for text in self.text_list:
                all_text += text + '\n\n'
            f.write(all_text)
        print("処理内容のファイル出力完了")

    # def update_customers(self, *args, **kwargs):
    #     print("更新func開始")
