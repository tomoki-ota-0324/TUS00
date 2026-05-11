from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.http import HttpResponse

from sfacd.gis.management.commands.create_customers import Command
from sfacd.gis.models import Shop2, GisCustomer
from sfacd.users.models import User

import time
import datetime

class ReadCsvView(TemplateView, LoginRequiredMixin):
    template_name = "gis/read_csv.html"
    output_file_path = Command().output_file_path
    only_read_columns = Command().only_read_columns
    #google map client
    gmaps = Command.gmaps #デフォルトでGoogleとHTTPS接続 https://github.com/googlemaps/google-maps-services-python/blob/master/googlemaps/client.py
    user_id_list = list(User.objects.all().values_list('id', flat=True)) #コマンドが作動した時点でDBに登録のあるユーザーのIDの入ったリスト
    shop_id_list = list(Shop2.objects.all().values_list('id', flat=True)) #コマンドが作動した時点でDBに登録のあるユーザーのIDの入ったリスト

    def get(self, request, *args, **kwargs):
        """
        superuser以外のユーザーがアクセスした場合はエラーを返し、superuserであればCSV読込画面を表示する
        """
        flg = False
        if request.user.is_superuser:
            flg = True
        if flg:
            context = super().get_context_data()
            return super().render_to_response(context)
        else:
            error_message = "利用権限が付与されていません。管理者より権限を頂いてください。"
            context = super().get_context_data(
                error_message=error_message
            )
            return super().response_class(
                request=self.request,
                template="gis/index.html",
                context=context,
                using=super().template_engine,
            )
        
    def post(self, request, *args, **kwargs):
        """
        クライアントから直接CSVを渡される時の読込処理
        """
        try:
            text_list = [] #処理結果をテキストファイルに出力するときに使用
            geocoding_count = 0
            before_time = time.time() #処理前の時刻
            now = datetime.datetime.now()
            st_now = now.strftime('%Y-%m-%d-%H%M%S')
            text = "処理開始：{}".format(datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
            print(text)
            text_list.append(text)
            csv_data = request.FILES['file'].file #リクエストからファイルを読込
            data, text_list = Command().read_csv(csv_data, text_list) #CSVからの読込と文字列正規化
            if data is None:
                raise ValueError("CSVの読込に失敗しました。指定されたI-CROP出力CSVを選択してください。")
            print("読込時間：{}".format(time.time() - before_time))
            text = "読込データ行数：{}行".format(str(len(data)))
            print(text)
            text_list.append(text)
            text = "user_id, shop_idが登録されておらず、登録出来なかった場合、これより以下に対象idが記されます。"
            print(text)
            text_list.append(text)
            text = "-------------------------------------------"
            print(text)
            text_list.append(text)

            create_list, update_list, text_list, geocoding_count = Command().check_duplication(data, text_list, geocoding_count) #読込CSVのDBとの重複CKと新規か更新かを判断

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
            text = "処理が完了しました。経過時間：{}秒".format(time.time() - before_time)
            text_list.append(text)
            print(text)
        except Exception as e:
            text = 'ExceptionError 発生：{}'.format(e)
            print(text)
            text_list.append(text)
        finally:
            file_name = st_now + '_result.txt'
            full_path = self.output_file_path + file_name
            Command().write_txt(file_name, text_list)
            with open(full_path, 'r', encoding='shift_jis', newline='\r\n') as f:
                response = HttpResponse(f.read(), content_type='text/plain')
                response['Content-Disposition'] = 'attachment; filename="{}"'.format(file_name)
                return response

