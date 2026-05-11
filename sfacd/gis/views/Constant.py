from django.views.generic import View
from sfacd.gis.models import Department

import os

class Constant(View):

    def __init__(self):
        self.FRONT_API = os.environ.get('LTSHttpLimitKey') # google http_limit_api_key
        self.SERVER_API = os.environ.get('LTSIPLimitKey') # google ip_limit_api_key
        # self.input_file_path = "./sfacd/sfacd/static/test/*.csv" #ローカルデバッグ環境用
        self.input_file_path = "./sfacd/static/test/*.csv" # ローカル環境用, 本番環境用
        self.output_file_path = "./sfacd/static/test/" # ローカル環境用, 本番環境用
        # self.output_file_path = "C:/Users/naoki.shinagawa/Envs/STP00-dev/sfacd/sfacd/static/test/"
        self.auth_department_list = Department.objects.filter(auth_flg=True).values_list('id', flat=True) #商圏分析機能アクセス許可リスト 11:店長 12:営業マネージャ 13:新車営業スタッフ 41:レクサス本部マネージャ 42:レクサス本部担当 51:本部マネージャ 52:本部担当 91:システム管理者
        self.only_read_columns = {
            'お客様コード': 'object', '性別区分': 'int64', '郵便番号': 'object', 'お客様住所漢字': 'object', '顧客固定客区分': 'int64', '顧客層別区分': 'int64', '登録ＮＯ.': 'object', '型式': 'object',
            '車名': 'object', '新中区分': 'int64', '軽区分': 'int64', '業直区分': 'int64', '車両固定客区分': 'int64', '車両層別区分': 'int64', '車検満了日': 'object', '保険満期日': 'object', '担当スタッフコード': 'int64',
            '担当スタッフ名': 'object', '担当店舗コード': 'int64', '担当店舗名': 'object', 'サービス店舗コード': 'int64', 'サービス店舗名': 'object',
            } #CSV読込機能のよっみこみ対象Header
        self.max_marker_icon_num = 36 #staticに用意されているマーカーの連番最大数
