from django.core.management import BaseCommand
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

from sfacd.gis.models import Shop2, GisCustomer
from sfacd.users.models import User
from sfacd.gis.views.Constant import Constant

import time
import csv
import datetime
import pandas
import numpy
import googlemaps
import re
import glob
import os
# from mojimoji import han_to_zen, zen_to_han #車名半角カタカナを直す必要があれば実施

class Command(BaseCommand):
    """
    カスタムコマンド
    """
    help = '読み込んだCSVのレコード一つ一つをDBレコードの車両No.とCKして、新規登録か、更新かを判断し実行する。'
    #定数
    input_file_path = Constant().input_file_path #仮設置パス
    output_file_path = Constant().output_file_path #処理経過テキストの出力先
    only_read_columns = Constant().only_read_columns #CSV読込対象カラムの辞書
    #google map client
    gmaps = googlemaps.Client(key=Constant().SERVER_API) #デフォルトでGoogleとHTTPS接続 https://github.com/googlemaps/google-maps-services-python/blob/master/googlemaps/client.py
    user_id_list = list(User.objects.all().values_list('id', flat=True)) #コマンドが作動した時点でDBに登録のあるユーザーのIDの入ったリスト
    shop_id_list = list(Shop2.objects.all().values_list('id', flat=True)) #コマンドが作動した時点でDBに登録のあるユーザーのIDの入ったリスト

    def add_arguments(self, parser): #コマンドのオプションを設定できる。引数を必要としない場合は、この関数の実装は必須ではない
        parser.add_argument('--delete', help='CSVになくDBのみのデータの削除処理も実施', action="store_true") #デフォルトはCSVとDB内の重複を除く、新規登録、更新のみ py manage.py create_customers --delete

    def handle(self, *args, **kwargs):
        """
        CSVより自動顧客情報取込み機能
        CSVの読み込んだレコードがDBに登録してあるデータに対し、車両登録No.がユニークであるか確認し、ユニークであれば新規登録、そうでなければ優先登録する方を判断し、更新登録させる。
        """
        try:
            text_list = [] #処理結果をテキストファイルに出力するときに使用
            geocoding_count = 0 #Geocodingを実施した件数を表示
            before_time = time.time() #処理前の時刻
            now = datetime.datetime.now()
            st_now = now.strftime('%Y-%m-%d-%H%M%S')
            text = "処理開始：{}".format(datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
            print(text)
            text_list.append(text)
            csv_list = glob.glob(self.input_file_path) #ディレクトリ内のCSVファイル一覧
            for path in csv_list: #ディレクトリ内のCSVファイルをすべてひとつづつ読み取り
                geocoding_count = 0 #カウントのリセット
                csv_abspath = os.path.abspath(path) #相対パスから絶対パスへの変換
                text = "##############################################################"
                print(text)
                text_list.append(text)
                text = "読込ファイル名：{}".format(csv_abspath)
                print(text)
                text_list.append(text)
                data, text_list = self.read_csv(csv_abspath, text_list) #CSVからの読込と文字列正規化
                if data is None:
                    raise ValueError("CSVの読込に失敗しました。指定されたI-CROP出力CSVを選択してください。")
                text = "読込データ行数：{}行".format(str(len(data)))
                print(text)
                text_list.append(text)
                # text = "user_id, shop_idが登録されておらず、登録出来なかった場合、これより以下に対象idが記されます。" # user_idのメンテナンスをしなくなったため内容変更
                text = "shop_idが登録されておらず、登録出来なかった場合、これより以下に対象idが記されます。"
                print(text)
                text_list.append(text)
                text = "-------------------------------------------"
                print(text)
                text_list.append(text)

                create_list, update_list, text_list, geocoding_count = self.check_duplication(data, text_list, geocoding_count, kwargs['delete']) #読込CSVのDBとの重複CKと新規か更新かを判断
                if kwargs['delete']: # True
                    delete_customers = GisCustomer.objects.filter(csv_flg=False) #CSVデータにて、新規作成、更新、比較処理されなかったDBに登録のあるデータ
                    delete_num = len(delete_customers) #削除対象データ数
                    delete_customers.delete() #削除処理
                GisCustomer.objects.all().update(csv_flg=False) #削除処理終了後、次の読み込み時のためにcsv_flgをFalseに戻す

                text = "-------------------------------------------"
                print(text)
                text_list.append(text)
                text = "合計処理件数：{}件".format(str(len(create_list) + len(update_list)))
                print(text)
                text_list.append(text)
                text = "　内新規作成されたデータ件数：{}件".format(str(len(create_list)))
                print(text)
                text_list.append(text)
                text = "　内更新されたデータ件数：{}件".format(str(len(update_list)))
                print(text)
                text_list.append(text)
                text = "　内CSV側データがDB側データより古いか、user_id, shop_idがマスタに登録されてない、顧客コード、登録No.ともに入力なしと判断されたデータ件数：{}件".format(str(len(data) - (len(create_list) + len(update_list))))
                print(text)
                text_list.append(text)
                text = "GeoCodingを実施した件数：{}件".format(str(geocoding_count))
                print(text)
                text_list.append(text)
                if kwargs['delete']: # True
                    text = "CSVにデータがなく、DBより削除されたデータ件数：{}件".format(str(delete_num))
                    print(text)
                    text_list.append(text)
                text = "処理が完了しました。経過時間：{}秒".format(time.time() - before_time)
                text_list.append(text)
                print(text)
        except Exception as e:
            if kwargs['delete']: #削除オプションがついている際に途中でエラーが発生した場合は、新規登録、更新はエラー発生時点まで実施されるが、削除はされない、flgだけ次の読込に備えFalseに戻す
                GisCustomer.objects.all().update(csv_flg=False)
            text = 'ExceptionError 発生：{}'.format(e)
            print(text)
            text_list.append(text)
        finally:
            self.write_txt(st_now + '_result.txt', text_list)

    def read_csv(self, csv_data, text_list):
        """
        CSV読込と文字列正規化処理
        csv_data: csv file
        text_list: log text list
        指定されているCSVと違うCSVが読み込まれた場合はdata = Noneを返す
        """
        try:
            text = "CSV読込開始"
            print(text)
            text_list.append(text)
            columns_list = list(self.only_read_columns.keys())
            data = pandas.read_csv(csv_data, encoding="UTF-8", usecols=columns_list, dtype='object', na_filter=False)
            #空、空白を欠損値(NaN)として扱わない、CP932でないと読み込めない文字がある -> UnicodeDecodeError: 'cp932' codec can't decode byte 0x85 in position 50: illegal multibyte sequence が発生したため、UTF-8を使用（22/10/31）
            # print(data['お客様住所漢字'])
            check_columns = list(data.columns) #現在のcolumns（ヘッダー）のみ
            keys = [k for k, v in self.only_read_columns.items() if v == 'int64'] #数値部分だけNaNを代入
            change_nun_dict = {}
            for key in keys:
                change_nun_dict[key] = numpy.nan #数値扱いしてよい列を指定
            for row in check_columns:
                data[row] = data[row].str.strip() #文字列前後に存在する空白を除去
            data = data.replace('', change_nun_dict, regex=True) #数値扱いしてよい列の空文字はNaNに入れ替え
                #     data[row].str.replace('\u3000', '', regex=True) #文字列中間に存在する空白を除去、正規表現=True
                # if self.only_read_columns[row] == 'int64': #もしInt型にしたいカラムなら ！！恐らくここが重い
                #     for index, value in enumerate(data[row]): #リストを展開して
                #         if value == '': #要素が空なら
                #             data.loc[index, row] = None # Noneを代入する
            # data = data.astype(self.only_read_columns) #型変換
            return data, text_list
        except ValueError:
            data = None
            return data, text_list

    def check_duplication(self, data, text_list, geocoding_count, delete_flg):
        """
        登録するCSVレコードとDBに登録されているレコードの重複をCKし、新規登録、更新、スキップを選ぶ
        data: pandas dataframe
        text_list: text log list
        geocoding_count: int
        """
        print('重複CK')
        create_list = [] #新規作成されたインスタンスを入れる
        update_list = [] #更新されたインスタンスを入れる
        header_index = list(self.only_read_columns.keys())
        # car_num_list = list(GisCustomer.objects.all().exclude(car_num__startswith='ZZZZ').values_list('car_num', flat=True)) #ダミーナンバーを除いた車両登録No.のリスト
        search_dict = {} # customer_code%car_num: "address%inspection_date%insurance_date"
        cars = GisCustomer.objects.all()
        for car in cars:
            search_dict = self.add_search_dict(search_dict, car) #辞書にDB比較条件を追加
        for index, row in data.iterrows():
            # print(row)
            customer_code = self.check_text_integer_len(row[header_index.index('お客様コード')], 9) #桁数CK
            car_num = row[header_index.index('登録ＮＯ.')] #車両登録No.
            csv_inspection_date = self.change_date_from_text(row[header_index.index('車検満了日')]) #形式変更 datetime.date型
            csv_insurance_date = self.change_date_from_text(row[header_index.index('保険満期日')]) #形式変更 datetime.date型
            if csv_inspection_date is False or csv_insurance_date is False: #Falseが入っていた場合
                text = "CSV顧客コード：{}の日付が入る列に日付、空文字以外のデータが入力されています。新規登録、更新対象として除外します。".format(customer_code)
                print(text)
                text_list.append(text)
                continue
            if customer_code is None and car_num == '': #お客様コードも登録No.も入力がない場合
                continue #完全に処理をスキップする
            if customer_code[0] == 'J': #I-CROPユーザー
                print('I-CROP')
                if car_num[0:4] == 'ZZZZ': #ダミー
                    print('ダミー')
                    search_key = customer_code + '%' + car_num #辞書から検索するキー
                    if search_key in search_dict:
                        print('お客様コード同じ、車両同じ、ダミー更新登録')
                        db_id = self.get_from_search_dict(search_dict, search_key, 'id') #辞書からID取得
                        car_num, text_list, geocoding_count = self.update_customer(row, db_id, text_list, geocoding_count) #更新登録 更新なので、比較リストに車両No.の追加などは不要
                        if not car_num is None:
                            update_list.append(car_num) #エラーで更新できなかった場合は更新リストに入れない、削除とカウント用、ダミーの同一番号が入っているので削除処理時注意
                    else:
                        print('新規登録')
                        customer, text_list, geocoding_count = self.create_customer(row, text_list, geocoding_count) #新規登録処理
                        if not customer is None:
                            search_dict = self.add_search_dict(search_dict, customer) #新規作成した分を比較辞書に追加
                            create_list.append(customer.car_num) #削除とカウント用
                else: #ダミーでない
                    print('ダミーでない')
                    search_key = car_num #辞書から検索するキー
                    if search_key in search_dict: #DBとの重複あり
                        db_customer_code = self.get_from_search_dict(search_dict, search_key, 'customer_code') #辞書から顧客コード取得
                        db_customer_code = self.check_text_integer_len(db_customer_code, 9) #長さCK
                        if db_customer_code is None: #顧客コードCK
                            text = "顧客コードのないレコードがDBに登録されています。DBレコードID：{}".format(db_id)
                            print(text)
                            text_list.append(text)
                            continue
                        if db_customer_code[0] == 'J' and (self.text_num_without_string(db_customer_code) <= self.text_num_without_string(customer_code)): #DBの顧客コードがI-CROPかつ、顧客コードがCSVの方が大きい
                            print('更新登録')
                            # ここでDB側がAIデータの場合の比較
                            db_id = self.get_from_search_dict(search_dict, search_key, 'id') #辞書からID取得
                            customer, text_list, geocoding_count = self.update_customer(row, db_id, text_list, geocoding_count) #更新登録 更新なので、比較リストに車両No.の追加などは不要
                            if not customer is None:
                                search_dict = self.add_search_dict(search_dict, customer) #新規登録顧客を追加
                                update_list.append(customer.car_num) #エラーで更新できなかった場合は更新リストに入れない
                        else: #顧客コードがAI21レコード、もしくは顧客コードがDBの方が大きい
                            print('登録しない')
                            # text_list.append(car_num) #不要
                            if delete_flg:
                                customer = GisCustomer.objects.get(car_num=car_num) #CSVに車両データあり、DBデータ削除不要
                                customer.csv_flg = True
                                customer.save()
                            continue
                    else: #DBとの重複なし
                        print('新規登録')
                        customer, text_list, geocoding_count = self.create_customer(row, text_list, geocoding_count) #新規登録処理
                        if not customer is None:
                            search_dict = self.add_search_dict(search_dict, customer) #新規作成した分を比較辞書に追加
                            create_list.append(customer.car_num) #削除とカウント用
            else: #AI21ユーザー　
                print('AI21')
                if car_num[0:4] == 'ZZZZ': #ダミー
                    print('ダミー')
                    search_key = customer_code + '%' + car_num #辞書から検索するキー
                    if search_key in search_dict:
                        print('お客様コード同じ、車両同じ、ダミー更新登録')
                        db_id = self.get_from_search_dict(search_dict, search_key, 'id') #辞書からID取得
                        car_num, text_list, geocoding_count = self.update_customer(row, db_id, text_list, geocoding_count) #更新登録 更新なので、比較リストに車両No.の追加などは不要
                        if not car_num is None:
                            update_list.append(car_num) #エラーで更新できなかった場合は更新リストに入れない、削除とカウント用、ダミーの同一番号が入っているので削除処理時注意
                    else:
                        print('新規登録')
                        customer, text_list, geocoding_count = self.create_customer(row, text_list, geocoding_count) #新規登録処理
                        if not customer is None:
                            search_dict = self.add_search_dict(search_dict, customer) #新規作成した分を比較辞書に追加
                            create_list.append(customer.car_num) #削除とカウント用
                else: #ダミーでない
                    print('ダミーでない')
                    search_key = car_num #辞書から検索するキー
                    if search_key in search_dict: #DBとの重複あり
                        db_customer_code = self.get_from_search_dict(search_dict, search_key, 'customer_code') #DB側の顧客コード
                        db_customer_code = self.check_text_integer_len(db_customer_code, 9) #長さCK
                        db_id = self.get_from_search_dict(search_dict, search_key, 'id') #DB側のID
                        if db_customer_code is None: #顧客コードCK
                            text = "顧客コードのないレコードがDBに登録されています。比較できないレコードID：{}".format(db_id)
                            print(text)
                            text_list.append(text)
                            continue #次のレコードの処理にスキップ
                        if db_customer_code[0] == 'J': #DBレコードがI-CROPユーザー
                            print('更新登録')
                            customer, text_list, geocoding_count = self.update_customer(row, db_id, text_list, geocoding_count) #更新登録 更新なので、比較リストに車両No.の追加などは不要
                            if not customer is None:
                                search_dict = self.add_search_dict(search_dict, customer) #新規登録顧客を追加
                                update_list.append(customer.car_num) #エラーで更新できなかった場合は更新リストに入れない
                        else:
                            print('DBレコードがAI21')
                            db_inspection_date = self.get_from_search_dict(search_dict, search_key, 'inspection_date') #DB側の車検日 datetime.date
                            db_insurance_date = self.get_from_search_dict(search_dict, search_key, 'insurance_date') #DB側の保険日 datetime.date
                            if csv_inspection_date is None and db_inspection_date is None: #車検満了日がどちらも入力されていない
                                print('車検日なし')
                                if csv_insurance_date is None and db_insurance_date is None: #保険満期日がどちらも入力されていない
                                    print('保険日なし')
                                    row_year = int(customer_code[0:2]) #CSV顧客コードの年
                                    row_month = int(customer_code[2:4]) #CSV顧客コードの月
                                    row_number = int(customer_code[4:9]) #CSV顧客コードの連番
                                    db_row_year = int(db_customer_code[0:2]) #DB顧客コードの年
                                    db_row_month = int(db_customer_code[2:4]) #DB顧客コードの月
                                    db_row_number = int(db_customer_code[4:9]) #DB顧客コードの連番
                                    if db_row_year < row_year: #年がCSVの方が大きい
                                        print('作成年が大きい')
                                        print('更新登録')
                                        customer, text_list, geocoding_count = self.update_customer(row, db_id, text_list, geocoding_count) #更新登録 更新なので、比較リストに車両No.の追加などは不要
                                        if not customer is None:
                                            search_dict = self.add_search_dict(search_dict, customer) #新規登録顧客を追加
                                            update_list.append(customer.car_num) #エラーで更新できなかった場合は更新リストに入れない
                                    elif db_row_year == row_year and db_row_month < row_month: #月がCSVの方が大きい
                                        print('作成月が大きい')
                                        print('更新登録')
                                        customer, text_list, geocoding_count = self.update_customer(row, db_id, text_list, geocoding_count) #更新登録 更新なので、比較リストに車両No.の追加などは不要
                                        if not customer is None:
                                            search_dict = self.add_search_dict(search_dict, customer) #新規登録顧客を追加
                                            update_list.append(customer.car_num) #エラーで更新できなかった場合は更新リストに入れない
                                    elif db_row_year == row_year and db_row_month == row_month and db_row_number <= row_number: #連番がCSVの方が大きい、もしくは一緒
                                        print('連番が大きい')
                                        print('更新登録')
                                        customer, text_list, geocoding_count = self.update_customer(row, db_id, text_list, geocoding_count) #更新登録 更新なので、比較リストに車両No.の追加などは不要
                                        if not customer is None:
                                            search_dict = self.add_search_dict(search_dict, customer) #新規登録顧客を追加
                                            update_list.append(customer.car_num) #エラーで更新できなかった場合は更新リストに入れない
                                    else: #CSVの方が小さい
                                        print('CSVの方がお客様コードが古い')
                                        print('登録しない')
                                        # text_list.append(car_num) #不要
                                        if delete_flg:
                                            customer = GisCustomer.objects.get(car_num=car_num) #CSVに車両データあり、DBデータ削除不要
                                            customer.csv_flg = True
                                            customer.save()
                                        continue
                                else:
                                    print('保険日あり')
                                    if db_insurance_date is None:
                                        print('DB側のみ保険日入力なし')
                                        print('更新登録')
                                        customer, text_list, geocoding_count = self.update_customer(row, db_id, text_list, geocoding_count) #更新登録 更新なので、比較リストに車両No.の追加などは不要
                                        if not customer is None:
                                            search_dict = self.add_search_dict(search_dict, customer) #新規登録顧客を追加
                                            update_list.append(customer.car_num) #エラーで更新できなかった場合は更新リストに入れない
                                    elif csv_insurance_date is None:
                                        print('CSV側のみ保険日入力なし')
                                        print('更新しない')
                                        # text_list.append(car_num) #不要
                                        if delete_flg:
                                            customer = GisCustomer.objects.get(car_num=car_num) #CSVに車両データあり、DBデータ削除不要
                                            customer.csv_flg = True
                                            customer.save()
                                        continue
                                    elif db_insurance_date <= csv_insurance_date: #CSVの保険日の方がDBより新しい日付の場合、もしくは一緒の日付
                                        print('CSV側の保険日が新しい')
                                        customer, text_list, geocoding_count = self.update_customer(row, db_id, text_list, geocoding_count) #更新登録 更新なので、比較リストに車両No.の追加などは不要
                                        if not customer is None:
                                            search_dict = self.add_search_dict(search_dict, customer) #新規登録顧客を追加
                                            update_list.append(customer.car_num) #エラーで更新できなかった場合は更新リストに入れない
                                    else:
                                        print('CSV側の保険日が古い')
                                        print('更新しない')
                                        # text_list.append(car_num) #不要
                                        if delete_flg:
                                            customer = GisCustomer.objects.get(car_num=car_num) #CSVに車両データあり、DBデータ削除不要
                                            customer.csv_flg = True
                                            customer.save()
                                        continue
                            else:
                                print('車検日あり')
                                if db_inspection_date is None:
                                    print('DB側のみ車検日入力なし')
                                    print('更新登録')
                                    customer, text_list, geocoding_count = self.update_customer(row, db_id, text_list, geocoding_count) #更新登録 更新なので、比較リストに車両No.の追加などは不要
                                    if not customer is None:
                                        search_dict = self.add_search_dict(search_dict, customer) #新規登録顧客を追加
                                        update_list.append(customer.car_num) #エラーで更新できなかった場合は更新リストに入れない
                                elif csv_inspection_date is None:
                                    print('CSV側のみ車検日入力なし')
                                    print('登録しない')
                                    # text_list.append(car_num) #不要
                                    if delete_flg:
                                        customer = GisCustomer.objects.get(car_num=car_num) #CSVに車両データあり、DBデータ削除不要
                                        customer.csv_flg = True
                                        customer.save()
                                    continue
                                elif db_inspection_date <= csv_inspection_date: #CSVの車検日の方がDBより新しい日付の場合
                                    print('CSV側の車検日が新しい')
                                    print('更新登録')
                                    customer, text_list, geocoding_count = self.update_customer(row, db_id, text_list, geocoding_count) #更新登録 更新なので、比較リストに車両No.の追加などは不要
                                    if not customer is None:
                                        search_dict = self.add_search_dict(search_dict, customer) #新規登録顧客を追加
                                        update_list.append(customer.car_num) #エラーで更新できなかった場合は更新リストに入れない
                                else:
                                    print('CSV側車検日が古い')
                                    print('登録しない')
                                    # text_list.append(car_num) #不要
                                    if delete_flg:
                                        customer = GisCustomer.objects.get(car_num=car_num) #CSVに車両データあり、DBデータ削除不要
                                        customer.csv_flg = True
                                        customer.save()
                                    continue
                    else: #DBとの重複なし
                        print('新規登録')
                        customer, text_list, geocoding_count = self.create_customer(row, text_list, geocoding_count) #新規登録処理
                        if not customer is None:
                            search_dict = self.add_search_dict(search_dict, customer) #新規登録顧客を追加
                            create_list.append(customer.car_num)
        return create_list, update_list, text_list, geocoding_count

    def create_customer(self, row, text_list, geocoding_count):
        """
        新規登録処理、住所が空白でなければGeocoding、そのあと新規登録、作成したインスタンスを返す
        row: pandas row
        text_list: text log list
        geocoding_count: int count of geocoding
        """
        print('新規登録開始')
        header_index = list(self.only_read_columns.keys()) #ヘッダーのリスト
        customer_code = self.check_text_integer_len(row[header_index.index('お客様コード')], 9) #桁数CK
        sex = self.check_nan_to_9(row[header_index.index('性別区分')]) #不明を９
        post_code = row[header_index.index('郵便番号')]
        address = row[header_index.index('お客様住所漢字')]
        customer_fixed_kind = self.check_nan_to_9(row[header_index.index('顧客固定客区分')]) #不明を９
        sale_flg = self.check_nan_to_9(row[header_index.index('新中区分')]) #不明を９
        mini_flg = self.check_nan(row[header_index.index('軽区分')]) #不使用
        direct_kind = self.check_nan(row[header_index.index('業直区分')]) #不使用
        car_fixed_kind = self.check_nan_to_9(row[header_index.index('車両固定客区分')]) #不明を９
        car_rank_id = self.check_nan_to_9(row[header_index.index('車両層別区分')]) #不明を９
        customer_rank_id = self.check_nan_to_9(row[header_index.index('顧客層別区分')]) #不明を９
        service_shop_id = self.check_nan(row[header_index.index('サービス店舗コード')])
        shop_id = self.check_nan(row[header_index.index('担当店舗コード')])
        user_id = self.check_nan(row[header_index.index('担当スタッフコード')])
        car_model = row[header_index.index('型式')]
        car_name = row[header_index.index('車名')]
        car_num = row[header_index.index('登録ＮＯ.')]
        inspection_date = self.change_date_from_text(row[header_index.index('車検満了日')]) #形式変更 datetime.date型
        insurance_date = self.change_date_from_text(row[header_index.index('保険満期日')]) #形式変更 datetime.date型
        if address == '' or address is None: #新規登録するレコードの住所が空白だった場合
            print('住所なし')
            customer = GisCustomer(
                customer_code=customer_code, sex=sex, post_code=post_code,
                address=address, customer_fixed_kind=customer_fixed_kind, car_num=car_num,
                sale_flg=sale_flg, mini_flg=mini_flg, direct_kind=direct_kind, car_fixed_kind=car_fixed_kind,
                car_rank_id=car_rank_id, customer_rank_id=customer_rank_id, service_shop_id=service_shop_id,
                shop_id=shop_id, user_id=user_id, car_model=car_model, car_name=car_name,
                inspection_date=inspection_date, insurance_date=insurance_date, csv_flg=True
            )
            customer.save() #Geocoding関連以外を登録
            print('住所なしで登録されました。')
        else:
            print('住所あり')
            try:
                if not user_id is None and not int(user_id) in self.user_id_list: #もしUserIDがNoneでなくDBのIDリストにも存在しない場合
                    # raise IntegrityError('担当スタッフコードが DB Userに存在しません。ID：{}'.format(user_id))
                    # 22/10/25 改修時に担当スタッフデータメンテナンスをしない方針になったため、取込CSVに記載されており、現時点でDBに存在しないユーザーIDはNULLに置換えにする（リレーションが貼られているため、バリデーションが発生し、単にIDをそのまま登録することはできない）
                    text = '担当スタッフコードが DB Userに存在しません。ID：{}, よって担当スタッフコードをNULLに置換えました。'.format(user_id)
                    print(text)
                    # text_list.append(text) # 22/10/31 改修時に担当スタッフデータメンテナンスをしない方針になったため、エラーとして扱わないので、結果出力ファイルに入れない
                    user_id = None
                elif not shop_id is None and not int(shop_id) in self.shop_id_list:
                    raise IntegrityError('担当店舗コードが DB Shop2に存在しません。ID：{}'.format(shop_id))
                elif not service_shop_id is None and not int(service_shop_id) in self.shop_id_list:
                    raise IntegrityError('サービス担当店舗が DB Shop2に存在しません。ID：{}'.format(service_shop_id)) #Geocodingの後にリレーションエラーが発生するとGeocodingがもったいないので、この時点で無理やり発生させる


                db_address = GisCustomer.objects.filter(post_code__isnull=False, address=address, lat__isnull=False, lng__isnull=False).first()
                if db_address is None:
                    #Geocoding ON OFF 切り替え

                    location, geocoding_count = self.get_location(address, geocoding_count)
                    lat = location[address]['lat']
                    lng = location[address]['lng']
                    google_address = location[address]['address']
                    rank = location[address]['location_rank']
                    partial_match = location[address]['partial_match']
                    location_rank = self.get_location_rank(rank) #rankを数値へ変換

                    # lat = None
                    # lng = None
                    # google_address = None
                    # partial_match = None
                    # location_rank = None
                else:
                    print('DBにGeocoding済み住所あり')
                    post_code = db_address.post_code
                    lat = db_address.lat
                    lng = db_address.lng
                    google_address = db_address.google_address
                    partial_match = db_address.partial_match
                    location_rank = db_address.location_rank

                customer = GisCustomer(
                    customer_code=customer_code, sex=sex, post_code=post_code,
                    address=address, customer_fixed_kind=customer_fixed_kind, car_num=car_num,
                    sale_flg=sale_flg, mini_flg=mini_flg, direct_kind=direct_kind, car_fixed_kind=car_fixed_kind,
                    car_rank_id=car_rank_id, customer_rank_id=customer_rank_id, service_shop_id=service_shop_id,
                    shop_id=shop_id, user_id=user_id, car_model=car_model, car_name=car_name,
                    inspection_date=inspection_date, insurance_date=insurance_date, lat=lat, lng=lng, google_address=google_address,
                    location_rank=location_rank, partial_match=partial_match, csv_flg=True,
                )
                customer.save() #全てを登録
                print('住所ありで登録されました。')
            except IntegrityError as e: #リレーションエラー
                text = 'IntegrityError 発生：{}'.format(e)
                print(text)
                text_list.append(text)
                customer = None
        print(customer)
        return customer, text_list, geocoding_count

    def update_customer(self, row, db_id, text_list, geocoding_count):
        """
        住所が空白でないか、DBレコード側の比較対象と住所が同じでないか確認し、違う住所であればGeocodingして、更新登録し、更新されたインスタンスを返す
        row: pandas row
        db_id: update giscustomer id
        text_list: text log list
        geocoding_count: int count of geocoding
        """
        print('更新登録開始')
        db_customer = GisCustomer.objects.get(id=int(db_id))
        header_index = list(self.only_read_columns.keys()) #ヘッダーのリスト
        customer_code = self.check_text_integer_len(row[header_index.index('お客様コード')], 9) #桁数CK
        sex = self.check_nan_to_9(row[header_index.index('性別区分')]) #不明を９
        post_code = row[header_index.index('郵便番号')]
        address = row[header_index.index('お客様住所漢字')]
        customer_fixed_kind = self.check_nan_to_9(row[header_index.index('顧客固定客区分')]) #不明を９
        sale_flg = self.check_nan_to_9(row[header_index.index('新中区分')]) #不明を９
        mini_flg = self.check_nan(row[header_index.index('軽区分')]) #不使用
        direct_kind = self.check_nan(row[header_index.index('業直区分')]) #不使用
        car_fixed_kind = self.check_nan_to_9(row[header_index.index('車両固定客区分')]) #不明を９
        car_rank_id = self.check_nan_to_9(row[header_index.index('車両層別区分')]) #不明を９
        customer_rank_id = self.check_nan_to_9(row[header_index.index('顧客層別区分')]) #不明を９
        service_shop_id = self.check_nan(row[header_index.index('サービス店舗コード')])
        shop_id = self.check_nan(row[header_index.index('担当店舗コード')])
        user_id = self.check_nan(row[header_index.index('担当スタッフコード')])
        car_model = row[header_index.index('型式')]
        car_name = row[header_index.index('車名')]
        inspection_date = self.change_date_from_text(row[header_index.index('車検満了日')]) #形式変更 datetime.date型
        insurance_date = self.change_date_from_text(row[header_index.index('保険満期日')]) #形式変更 datetime.date型
        try:
            if not user_id is None and not int(user_id) in self.user_id_list: #もしUserIDがNoneでなくDBのIDリストにも存在しない場合
                # raise IntegrityError('担当スタッフコードが DB Userに存在しません。ID：{}'.format(user_id))
                # 22/10/25 改修時に担当スタッフデータメンテナンスをしない方針になったため、取込CSVに記載されており、現時点でDBに存在しないユーザーIDはNULLに置換えにする（リレーションが貼られているため、バリデーションが発生し、単にIDをそのまま登録することはできない）
                text = '担当スタッフコードが DB Userに存在しません。ID：{}, よって担当スタッフコードをNULLに置換えました。'.format(user_id)
                print(text)
                # text_list.append(text) # 22/10/31 改修時に担当スタッフデータメンテナンスをしない方針になったため、エラーとして扱わないので、結果出力ファイルに入れない
                user_id = None
            elif not shop_id is None and not int(shop_id) in self.shop_id_list:
                raise IntegrityError('担当店舗コードが DB Shop2に存在しません。ID：{}'.format(shop_id))
            elif not service_shop_id is None and not int(service_shop_id) in self.shop_id_list:
                raise IntegrityError('サービス担当店舗が DB Shop2に存在しません。ID：{}'.format(service_shop_id)) #Geocodingの後にリレーションエラーが発生するとGeocodingがもったいないので、この時点で無理やり発生させる
            if address == '' or address is None: #更新登録するレコードの住所が空白だった場合
                print('住所なし')
                db_customer.customer_code = customer_code
                db_customer.sex = sex
                db_customer.customer_fixed_kind = customer_fixed_kind
                db_customer.sale_flg = sale_flg
                db_customer.mini_flg = mini_flg
                db_customer.direct_kind = direct_kind
                db_customer.car_fixed_kind = car_fixed_kind
                db_customer.car_rank_id = car_rank_id
                db_customer.customer_rank_id = customer_rank_id
                db_customer.service_shop_id = service_shop_id
                db_customer.shop_id = shop_id
                db_customer.user_id = user_id
                db_customer.car_model = car_model
                db_customer.car_name = car_name
                db_customer.inspection_date = inspection_date
                db_customer.insurance_date = insurance_date
                db_customer.csv_flg = True
                db_customer.save() #Geocodingなしで更新
                print('住所そのまま、Geocodingなしで更新登録されました。')
            else:
                print('住所あり')
                if address == db_customer.address:
                    print('住所が一緒')
                    db_customer.customer_code = customer_code
                    db_customer.sex = sex
                    db_customer.customer_fixed_kind = customer_fixed_kind
                    db_customer.sale_flg = sale_flg
                    db_customer.mini_flg = mini_flg
                    db_customer.direct_kind = direct_kind
                    db_customer.car_fixed_kind = car_fixed_kind
                    db_customer.car_rank_id = car_rank_id
                    db_customer.customer_rank_id = customer_rank_id
                    db_customer.service_shop_id = service_shop_id
                    db_customer.shop_id = shop_id
                    db_customer.user_id = user_id
                    db_customer.car_model = car_model
                    db_customer.car_name = car_name
                    db_customer.inspection_date = inspection_date
                    db_customer.insurance_date = insurance_date
                    db_customer.csv_flg = True
                    db_customer.save() #Geocodingなしで更新
                    print('住所一緒、Geocodingなしで更新されました。')
                else:
                    print('住所が別')
                    db_address = GisCustomer.objects.filter(post_code__isnull=False, address=address, lat__isnull=False, lng__isnull=False).first()
                    if db_address is None:
                        # Geocoding ON OFF 切り替え

                        location, geocoding_count = self.get_location(address, geocoding_count)
                        lat = location[address]['lat']
                        lng = location[address]['lng']
                        google_address = location[address]['address']
                        rank = location[address]['location_rank']
                        location_rank = self.get_location_rank(rank) #rankを数値へ変換
                        partial_match = location[address]['partial_match']

                        # lat = None
                        # lng = None
                        # google_address = None
                        # location_rank = None
                        # partial_match = None
                    else:
                        print('DBにGeocoding済み住所あり')
                        post_code = db_address.post_code
                        lat = db_address.lat
                        lng = db_address.lng
                        google_address = db_address.google_address
                        partial_match = db_address.partial_match
                        location_rank = db_address.location_rank

                    db_customer.customer_code = customer_code
                    db_customer.sex = sex
                    db_customer.post_code = post_code
                    db_customer.address = address
                    db_customer.customer_fixed_kind = customer_fixed_kind
                    db_customer.sale_flg = sale_flg
                    db_customer.mini_flg = mini_flg
                    db_customer.direct_kind = direct_kind
                    db_customer.car_fixed_kind = car_fixed_kind
                    db_customer.car_rank_id = car_rank_id
                    db_customer.customer_rank_id = customer_rank_id
                    db_customer.service_shop_id = service_shop_id
                    db_customer.shop_id = shop_id
                    db_customer.user_id = user_id
                    db_customer.car_model = car_model
                    db_customer.car_name = car_name
                    db_customer.inspection_date = inspection_date
                    db_customer.insurance_date = insurance_date
                    db_customer.lat = lat
                    db_customer.lng = lng
                    db_customer.google_address = google_address
                    db_customer.location_rank = location_rank
                    db_customer.partial_match = partial_match
                    db_customer.csv_flg = True
                    db_customer.save() #Geocodingして全て更新
                    print('住所別、Geocodingありで更新されました。')
        except IntegrityError as e: #リレーションエラー
            text = 'IntegrityError 発生：{}'.format(e)
            print(text)
            text_list.append(text)
            db_customer = None
        print(db_customer)
        return db_customer, text_list, geocoding_count

    def get_location(self, text_location, geocoding_count):
        '''
        送られてきた場所名を引数に、緯度、経度を、その名前とともに返す
        text_location: String
        geocoding_count: Geocoding回数のカウント
        return {地名: {lat: lat_num, lng: lng_num}}, geocoding_count:int
        '''
        location_dict = {}
        print(text_location)
        if text_location == "":
            location_dict = {text_location: {"lat": None, "lng": None, "address": "", "location_rank": None, "partial_match": None}}
        else:
            geo_result = self.gmaps.geocode(address=text_location, language='ja')
            geocoding_count += 1 #Geocoding実行カウント
            if len(geo_result) == 0:
                location_dict = {text_location: {"lat": None, "lng": None, "address": "", "location_rank": None, "partial_match": None}}
            else:
                location = geo_result[0]['geometry']['location'] #緯度経度
                location['address'] = geo_result[0]['formatted_address'] #正規化住所
                location['location_rank'] = geo_result[0]['geometry']['location_type'] #出力ランク
                if 'partial_match' in geo_result[0].keys():
                    location['partial_match'] = True #部分一致で返された住所の場合 True
                else:
                    location['partial_match'] = False
                location_dict[text_location] = location
        return location_dict, geocoding_count #{検索名: {lat: lat_num, lng: lng_num, address: japanese_address, location_rank: 'ROOFTOP', partial_match: False}}

    def write_txt(self, file_name, text_list):
        """
        処理経過を書き出す、特に必要なマスターデータの変更など
        """
        with open(self.output_file_path + file_name, mode="w", encoding="utf-8") as f:
            all_text = ""
            for text in text_list:
                all_text += text + '\r\n\r\n'
            f.write(all_text)
        print("処理内容のファイル出力完了")

    def get_location_rank(self, rank):
        """
        google geocodeingから返された緯度経度変換ランクを文字列から数値に置き換えて返す
        """
        if rank == "ROOFTOP":
            location_rank = 4
        elif rank == "RANGE_INTERPOLATED":
            location_rank = 3
        elif rank == "GEOMETRIC_CENTER":
            location_rank = 2
        elif rank == "APPROXIMATE":
            location_rank = 1
        else:
            location_rank = None
        return location_rank

    def change_date_from_text(self, text_date):
        """
        テキスト日付を受け取り、空文字ならNone, 2019/01/01の表記ならdatetime.date型で返す
        """
        if text_date == '' or text_date == 'None':
            tdate = None
        elif re.match('[A-Z]\d{1,3}\.\d{1,2}\.\d{1,2}$', text_date) is None and re.match('^\d{4}/\d{1,2}/\d{1,2}$', text_date) is None and re.match('^\d{4}-\d{1,2}-\d{1,2}$', text_date) is None:
            tdate = False #不明な文字が入っている
        elif not re.match('[A-Z]\d{1,3}\.\d{1,2}\.\d{1,2}$', text_date) is None and re.match('^\d{4}/\d{1,2}/\d{1,2}$', text_date) is None and re.match('^\d{4}-\d{1,2}-\d{1,2}$', text_date) is None:
            raise Exception('CSVの日付データが和暦表示(H〇〇.〇〇.〇〇)となっています。\nデータを修正して再度読み込ませてください。') #"H31.10.10"を想定
        elif re.match('^\d{4}/\d{1,2}/\d{1,2}$', text_date) is None and not re.match('^\d{4}-\d{1,2}-\d{1,2}$', text_date) is None: #2018-10-10のハイフン形式に当てはまるもの
            tdatetime = datetime.datetime.strptime(text_date, '%Y-%m-%d') #DBからのデータ形式
            tdate = datetime.date(tdatetime.year, tdatetime.month, tdatetime.day)
        else:
            tdatetime = datetime.datetime.strptime(text_date, '%Y/%m/%d') #CSVからのデータ形式
            tdate = datetime.date(tdatetime.year, tdatetime.month, tdatetime.day)
        return tdate

    def check_text_integer_len(self, text_num, len_num):
        """
        与えられた文字列数値(text_num)が、与えられた桁数(len_num)と一致しなければ、桁数を修正し返す、空文字ならNoneを返す
        """
        if text_num == '': #空文字の場合
            text_num = None
        elif text_num[0] == 'J': #I-CROPの場合
            text_num
        else:
            text = re.sub(r"\d", "", text_num) # 数字以外
            num = re.sub(r"\D", "", text_num) # 数字のみ
            if len(num) < len_num: #9桁に足りない場合
                text_num = num.zfill(len_num) + text #9桁になるまで頭に0をつける、除いたアルファベットをつなげる
        return text_num

    def add_search_dict(self, search_dict, car):
        """
        DBレコードデータで比較対象辞書に追加する
        car_numがダミーの場合のキーは、{customer_code%car_num: "address%inspection_date%insurance_date, ....}
        それ以外のキーはcar_num
        """
        giscustomer_id = car.id
        customer_code = car.customer_code
        car_num = car.car_num
        address = car.address
        inspection_date = car.inspection_date
        insurance_date = car.insurance_date
        if customer_code is None:
            customer_code = "None"
        if car_num is None:
            car_num = "None"
        if address is None:
            address = "None"
        if inspection_date is None:
            inspection_date = "None"
        if insurance_date is None:
            insurance_date = "None"
        if car_num[0:4] == 'ZZZZ':
            key = str(customer_code) + "%" + str(car_num)
        else:
            key = car_num
        value = str(giscustomer_id) + "%" + str(customer_code) + "%" + str(address) + "%" + str(inspection_date) + "%" + str(insurance_date)
        search_dict[key] = value
        return search_dict

    def get_from_search_dict(self, search_dict, key, column):
        """
        比較対象辞書から住所、車検日(date型)、保険日(date型)に変更する
        """
        value = search_dict[key]
        value_list = value.split('%')
        if column == 'id':
            item = value_list[0]
        if column == 'customer_code':
            item = value_list[1]
        elif column == 'address':
            item = value_list[2]
        elif column == 'inspection_date':
            item = self.change_date_from_text(value_list[3])
        elif column == 'insurance_date':
            item = self.change_date_from_text(value_list[4])
        return item

    def check_nan(self, one):
        """
        one: nan or objects
        change nan to None
        """
        if type(one) != str:
            if numpy.isnan(one):
                one = None
        return one

    def check_nan_to_9(self, one):
        """
        one: non or objects
        change nan to 9
        """
        if type(one) != str:
            if numpy.isnan(one):
                one = 9
        return one

    def text_num_without_string(self, text_num):
        """
        text_num: J12345678, J12345678a, 191200001, 191200002b
        """
        num = re.sub("\\D", "", text_num)
        return int(num)
