from django.db import models

# Create your models here.

class TimestampedModel(models.Model):
    create_date = models.DateTimeField('作成日時', auto_now_add=True)    #作成日時を自動保存
    create_user = models.CharField('作成者', max_length=20, blank=True, default='')
    modify_date = models.DateTimeField('更新日時', auto_now=True)        #更新日時を自動保存
    modify_user = models.CharField('更新者', max_length=20, blank=True, default='')

    class Meta:
        abstract = True

class Customer(models.Model):
    post_code = models.IntegerField('郵便番号', default=0000000) #入力なし：0000000
    address = models.CharField('住所', max_length=100, default='不明') #入力なし：不明
    staff_shop_id = models.IntegerField('スタッフ所属店舗ID', default=999) #入力なし：999
    sale_shop_id = models.IntegerField('販売店舗ID', default=999) #入力なし：999
    servise_shop_id = models.IntegerField('サービス店舗ID', default=999) #入力なし：999
    staff_id = models.IntegerField('スタッフID', default=999999) #入力なし：999999
    sale_kind = models.IntegerField('販売区分', default=99) #新車: 1, U-Car: 2, 入力なし：99
    lat = models.FloatField('緯度', max_length=20, default=0.00) #短い数値の方　例：35.0000
    lng = models.FloatField('経度', max_length=20, default=0.00) #長い数値の方　例：138.000
    rank_kind = models.CharField('顧客層', max_length=10, default="", blank=True, null=True) #入力なし：空
    inspection_date = models.DateField('車検満了日', blank=True, null=True) #入力なし：空
    car_type = models.CharField('車種', max_length=100, default="", blank=True, null=True) #入力なし：空
    last_contact_date = models.DateField('最終接触日', blank=True, null=True) #入力なし：空
    car_registration_date = models.DateField('初回登録日', blank=True, null=True) #入力なし：空

    def __str__(self):
        return u'%s' % (self.address)

class Shop(models.Model):
    name = models.CharField('店舗名', max_length=100, default='不明') #入力なし：不明
    address = models.CharField('住所', max_length=100, default='不明') #入力なし：不明
    lat = models.FloatField('緯度', max_length=20, default=0.00) #短い数値の方　例：35.0000
    lng = models.FloatField('経度', max_length=20, default=0.00) #長い数値の方　例：138.000
    shop_type = models.IntegerField('店舗種類', default=0) #新車:0, U-Car:1, レクサス:2, その他(部署など):3
    shop_flg = models.BooleanField('実店舗', default=1) #店舗:1(true), 部署:0(false)
    # marker_path = models.CharField('マーカー', max_length=100, default='sample.png') #マーカーに使う画像の名前

    def __str__(self):
        return u'%s' % (self.name)

class Mylist(TimestampedModel):
    title = models.CharField('タイトル', max_length=100, blank=False)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE) #User.model　リレーション
    customers = models.ManyToManyField(Customer) # Mylist-obj.customers.all()で取得可能、逆はCustomer-obj.mylist_set.all()で取得

    def __str__(self):
        return u'%s' % (self.title)


#--------------営業支援機能側モデル-------------------------------------------------------------------

#integer, floatだとブランクダメ、

class Rank(models.Model):
    class Meta:
        verbose_name_plural = 'ランク層マスタデータ'

    id = models.IntegerField('客層区分', primary_key=True)
    rank = models.CharField('客層', max_length=100, blank=True, null=True)

    def __str__(self):
        return u'%s' % (self.rank)

class BaseCustomer(models.Model):
    id = models.CharField('顧客コード', max_length=100, primary_key=True)
    name = models.CharField('顧客名', max_length=100, blank=True, null=True)
    sex = models.IntegerField('性区分', blank=True, null=True)
    post_code = models.CharField('郵便番号', max_length=100, blank=True, null=True)
    address = models.CharField('住所', max_length=100, blank=True, null=True)
    tel = models.CharField('電話番号', max_length=100, blank=True, null=True)
    dm_flg = models.NullBooleanField('顧客DM可否', null=True, blank=True)
    list_flg = models.NullBooleanField('顧客リスト可否', null=True, blank=True)
    tel_flg = models.NullBooleanField('顧客tel可否', null=True, blank=True)
    email_flg = models.NullBooleanField('顧客email可否', null=True, blank=True)
    fixed_kind = models.IntegerField('顧客固定客区分', blank=True, null=True)
    rank = models.ForeignKey(Rank, on_delete=models.SET_NULL, null=True, verbose_name='顧客層別区分')
    lat = models.FloatField('緯度', blank=True, null=True)
    lng = models.FloatField('経度', blank=True, null=True)

    def __str__(self):
        return u'%s' % (self.name)

class CustomerDetail(models.Model):
    base_customer = models.OneToOneField(BaseCustomer, on_delete=models.CASCADE, primary_key=True)
    name_kana = models.CharField('顧客名カナ', max_length=100, blank=True, null=True)
    birthday = models.DateField('生年月日', blank=True, null=True)
    email = models.CharField('Eメールアドレス', max_length=100, blank=True, null=True)
    cellphone = models.CharField('携帯電話番号', max_length=100, blank=True, null=True)
    company_phone = models.CharField('勤務先TEL', max_length=100, blank=True, null=True)
    company_name = models.CharField('勤務先名', max_length=100, blank=True, null=True)
    return_dm_num = models.IntegerField('DM返却回数', blank=True, null=True)
    best_way = models.CharField('最適方法', max_length=100, blank=True, null=True)
    best_often = models.CharField('最適頻度', max_length=100, blank=True, null=True)
    best_contact = models.CharField('最適連絡先', max_length=100, blank=True, null=True)
    best_time = models.CharField('最適時間', max_length=100, blank=True, null=True)
    best_day = models.CharField('最適曜日', max_length=100, blank=True, null=True)
    best_date = models.CharField('最適日付', max_length=100, blank=True, null=True) #入力データが日付でなかったので、一旦CharFieldで処理

    def __str__(self):
        return u'%s' % (self.name_kana)

class Shop2(models.Model): #マスタテーブル
    class Meta:
        verbose_name_plural = '店舗マスタデータ'

    # id = models.IntegerField('店舗コード', primary_key=True, help_text='店舗コードは一意（ユニーク）でなければいけません。半角数字で入力してください。トヨペットは規定店舗コード、カローラは1000からの連番、ネッツは2000からの連番、候補地は3000からの連番で入力してください。')
    id = models.IntegerField('店舗コード', primary_key=True, help_text='店舗コードはシステム内で一意（ユニーク）でかつ半角数字でなければいけません。トヨタユナイテッド静岡店舗は規定店舗コード（アルファベットがIDに含まれる場合は数値に置き換え）、候補地は3000番台からの連番で入力してください。') # 22/11/1 会社統合により変更
    name = models.CharField('店舗名', max_length=100, blank=True, null=True, help_text='候補地の場合も適当な名前を入力してください。')
    post_code = models.CharField('郵便番号', max_length=100, blank=True, null=True)
    address = models.CharField('住所', max_length=100, blank=True, null=True)
    tel = models.CharField('電話番号', max_length=100, blank=True, null=True)
    new_flg = models.NullBooleanField('新車部門あり', null=True, blank=True, help_text='候補地の場合も予定される販売部門を”はい”にしてください。')
    ucar_flg = models.NullBooleanField('中古車部門あり', null=True, blank=True, help_text='候補地の場合も予定される販売部門を”はい”にしてください。')
    service_flg = models.NullBooleanField('サービス部門あり', null=True, blank=True)
    brand_id = models.IntegerField('ブランド販売店コード', blank=True, null=True, help_text='トヨタ系は"14601", レクサス系は"24653からの連番"を入力してください。候補地の場合も予定されるブランド販売店コードを入力してください。')
    lat = models.FloatField('緯度', blank=True, null=True, help_text='緯度経度は実店舗の場合は必ず入力してください。')
    lng = models.FloatField('経度', blank=True, null=True, help_text='緯度経度は実店舗の場合は必ず入力してください。')
    shop_flg = models.NullBooleanField('実店舗', null=True, blank=True, help_text='候補地を含む実店舗の場合は「はい」、部署などの場合は「いいえ」にしてください。（「はい」を選択の場合のみ地図上に表示可能です。「はい」を選んだ場合は緯度経度の入力が必須です。）')
    # shop_kind = models.IntegerField('販売店舗種別', help_text='半角数字で入力してください。トヨペット店は"1", カローラ東海店は"2", ネッツトヨタスルガ店は"3", 候補地として利用は"4"を入力してください。')
    shop_kind = models.IntegerField('販売店舗種別', help_text='半角数字で入力してください。トヨタユナイテッド静岡店は"1", 候補地として利用は"4"を入力してください。') # 22/11/1 会社統合により変更


    def __str__(self):
        return u'%s' % (self.name)

class Shop2Detail(models.Model): #マスタテーブル　入力任意
    class Meta:
        verbose_name_plural = '店舗基本情報データ'

    shop = models.OneToOneField(Shop2, on_delete=models.CASCADE, primary_key=True, related_name="shop_detail")
    open_year_month = models.CharField('開設年月', max_length=25, null=True, blank=True, help_text='例:　2019年4月')
    build_passed_year = models.IntegerField('築年数', null=True, blank=True, help_text='半角数字で入力してください。')
    notices = models.CharField('特記事項', max_length=100, null=True, blank=True)
    shop_area = models.CharField('自社面積㎡,自社面積坪', max_length=50, null=True, blank=True, help_text='こちらに"自社面積㎡,自社面積坪"のようにカンマ区切りで半角数字で入力してください。(例：660㎡の200坪の場合　660,200 )')
    chinshaku_area = models.CharField('賃借面積㎡,賃借面積坪', max_length=50, null=True, blank=True, help_text='こちらに"自社面積㎡,自社面積坪"のようにカンマ区切りで半角数字で入力してください。(例：660㎡の200坪の場合　660,200 )')
    place_rent = models.IntegerField('土地賃料(千円)', null=True, blank=True, help_text='半角数字で入力してください。')
    building_area = models.CharField('建物面積㎡,建物面積坪', max_length=50, null=True, blank=True, help_text='こちらに"自社面積㎡,自社面積坪"のようにカンマ区切りで半角数字で入力してください。(例：660㎡の200坪の場合　660,200 )')
    floor_area = models.CharField('延床面積㎡,延床面積坪', max_length=50, null=True, blank=True, help_text='こちらに"自社面積㎡,自社面積坪"のようにカンマ区切りで半角数字で入力してください。(例：660㎡の200坪の場合　660,200 )')
    building_rent = models.IntegerField('建物賃料(千円)', null=True, blank=True, help_text='半角数字で入力してください。')
    youto_chiiki = models.CharField('用途地域', max_length=25, null=True, blank=True)
    factory_area = models.IntegerField('工場面積㎡', null=True, blank=True, help_text='半角数字で入力してください。')
    factory_auth = models.CharField('工場認可', max_length=25, null=True, blank=True)
    stalls = models.IntegerField('ストール数', null=True, blank=True, help_text='半角数字で入力してください。')
    members = models.CharField('店舗人員', max_length=100, null=True, blank=True,
        help_text='こちらにカンマ区切りで "店員総数,　店長/GM,　副店長,　営業TM,　QA/SC,　STM,　SAD/TM,　EL/WSL,　SE/TS,　FC/RS,　その他" の順番で入力してください。特定の業務スタッフがいない場合は0を入れカンマで区切り、次の業務スタッフ人数を続けて入力してください。\n例： 10,1,1,4,2,0,1,1,0,0,0')
    Y_3 = models.CharField('-3年度営業実績', null=True, blank=True, max_length=100,
        help_text='現在より3年前の営業実績を　"お客様数,　SA層比率(%),　新車販売台数,　U-Car販売台数,　総整備台数,　車検台数"　の順番でカンマ区切りで順番に入力してください。(例：5340,75,264,0,136,184)')
    Y_2 = models.CharField('-2年度営業実績', null=True, blank=True, max_length=100,
        help_text='現在より2年前の営業実績を　"お客様数,　SA層比率(%),　新車販売台数,　U-Car販売台数,　総整備台数,　車検台数"　の順番でカンマ区切りで順番に入力してください。(例：5340,75,264,0,136,184)')
    Y_1 = models.CharField('-1年度営業実績', null=True, blank=True, max_length=100,
        help_text='現在より1年前の営業実績を　"お客様数,　SA層比率(%),　新車販売台数,　U-Car販売台数,　総整備台数,　車検台数"　の順番でカンマ区切りで順番に入力してください。(例：5340,75,264,0,136,184)')
    close_store_P = models.CharField('近隣店舗P', max_length=50, null=True, blank=True)
    close_store_C = models.CharField('近隣店舗C', max_length=50, null=True, blank=True)
    close_store_N = models.CharField('近隣店舗N', max_length=50, null=True, blank=True)
    remarks = models.CharField('備考', max_length=100, null=True, blank=True)
    feature_store = models.CharField('店舗の将来像', max_length=150, null=True, blank=True)

    def __str__(self):
        return u'%s' % (self.shop.name)

class Car(models.Model): #マスタテーブル
    id = models.CharField('型式', max_length=100, primary_key=True)
    name = models.CharField('車名', max_length=100, blank=True, null=True)

    def __str__(self):
        return u'%s' % (self.name)

class CustomerCars(models.Model):
    car_num = models.CharField('車両登録No.', max_length=100, blank=True, null=True)
    base_customer = models.ForeignKey(BaseCustomer, on_delete=models.CASCADE, verbose_name='オーナー顧客')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, verbose_name='車両')
    dm_flg = models.NullBooleanField('顧客DM可否', null=True, blank=True)
    list_flg = models.NullBooleanField('顧客リスト可否', null=True, blank=True)
    tel_flg = models.NullBooleanField('顧客tel可否', null=True, blank=True)
    email_flg = models.NullBooleanField('顧客email可否', null=True, blank=True)
    sale_flg = models.NullBooleanField('新中区分', null=True, blank=True)
    mini_flg = models.NullBooleanField('軽区分', null=True, blank=True)
    direct_kind = models.IntegerField('業直区分', blank=True, null=True)
    fixed_kind = models.IntegerField('車両固定客区分', blank=True, null=True)
    rank = models.ForeignKey(Rank, on_delete=models.SET_NULL, null=True, verbose_name='顧客層別区分')
    registraction_date = models.DateField('初度登録日', blank=True, null=True)
    ucar_registraction_date = models.DateField('UCar初度登録日', blank=True, null=True)
    inspection_date = models.DateField('車検満了日', blank=True, null=True)
    insurance_date = models.DateField('保険満了日', blank=True, null=True)
    user = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, verbose_name='担当スタッフ')
    shop = models.ForeignKey(Shop2, on_delete=models.SET_NULL, null=True, verbose_name='担当店舗')
    sale_kind = models.CharField('販売区分', max_length=100, blank=True, null=True)
    sale_user = models.CharField('販売スタッフ', max_length=100, blank=True, null=True)
    sale_shop = models.CharField('販売店舗', max_length=100, blank=True, null=True)
    service_shop_id = models.IntegerField('サービス店舗', blank=True, null=True)
    receipt_date_1 = models.DateField('入庫歴_清算日１', blank=True, null=True)
    receipt_kind_1 = models.IntegerField('入庫歴_入庫区分１', blank=True, null=True)
    receipt_shop_1 = models.IntegerField('入庫歴_店舗', blank=True, null=True)
    receipt_date_2 = models.DateField('入庫歴_清算日１', blank=True, null=True)
    receipt_kind_2 = models.IntegerField('入庫歴_入庫区分１', blank=True, null=True)
    receipt_shop_2 = models.IntegerField('入庫歴_店舗', blank=True, null=True)
    receipt_date_3 = models.DateField('入庫歴_清算日１', blank=True, null=True)
    receipt_kind_3 = models.IntegerField('入庫歴_入庫区分１', blank=True, null=True)
    receipt_shop_3 = models.IntegerField('入庫歴_店舗', blank=True, null=True)
    receipt_date_4 = models.DateField('入庫歴_清算日１', blank=True, null=True)
    receipt_kind_4 = models.IntegerField('入庫歴_入庫区分１', blank=True, null=True)
    receipt_shop_4 = models.IntegerField('入庫歴_店舗', blank=True, null=True)
    receipt_date_5 = models.DateField('入庫歴_清算日１', blank=True, null=True)
    receipt_kind_5 = models.IntegerField('入庫歴_入庫区分１', blank=True, null=True)
    receipt_shop_5 = models.IntegerField('入庫歴_店舗', blank=True, null=True)
    address = models.CharField('住所', max_length=100, blank=True, null=True)
    lat = models.FloatField('緯度', blank=True, null=True)
    lng = models.FloatField('経度', blank=True, null=True)

    def __str__(self):
        return u'%s' % (self.id)

class Activity(models.Model): #マスタテーブル
    brand_id = models.IntegerField('ブランド販売店コード', blank=True, null=True)
    kind = models.IntegerField('活動項目区分', blank=True, null=True)
    name = models.CharField('活動項目名', max_length=100, blank=True, null=True)

    def __str__(self):
        return u'%s' % (self.name)

class ContactPartner(models.Model): #マスタテーブル
    brand_id = models.IntegerField('ブランド販売店コード', blank=True, null=True)
    kind = models.IntegerField('接触相手区分', blank=True, null=True)
    name = models.CharField('接触相手名', max_length=100, blank=True, null=True)

    def __str__(self):
        return u'%s' % (self.name)

class ContactWay(models.Model): #マスタテーブル
    brand_id = models.IntegerField('ブランド販売店コード', blank=True, null=True)
    kind = models.IntegerField('接触方法区分', blank=True, null=True)
    name = models.CharField('接触方法名', max_length=100, blank=True)

    def __str__(self):
        return u'%s' % (self.name)

class ContactResult(models.Model): #マスタテーブル
    brand_id = models.IntegerField('ブランド販売店コード', blank=True, null=True)
    kind = models.CharField('活動結果コード', max_length=100, blank=True, null=True)
    name = models.CharField('活動結果名', max_length=100, blank=True, null=True)

    def __str__(self):
        return u'%s' % (self.name)

class DailyPlan(models.Model):
    shop = models.ForeignKey(Shop2, on_delete=models.SET_NULL, null=True, verbose_name='活動店舗')
    user = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, verbose_name='担当スタッフ')
    plan_date = models.DateField('計画日', blank=True, null=True)
    base_customer_id = models.CharField('顧客コード', max_length=100, blank=True, null=True)
    car_num = models.CharField('車両登録No.', max_length=100, blank=True, null=True)
    activity_kind = models.IntegerField('活動項目区分', blank=True, null=True)
    limit_date = models.DateField('活動期限年月日', blank=True, null=True)
    registration_kind = models.IntegerField('発生元区分', blank=True, null=True)

    def __str__(self):
        return u'%s' % (self.plan_date)

# class DailyResult(models.Model):
#     shop = models.ForeignKey(Shop2, on_delete=models.SET_NULL, null=True, verbose_name='活動店舗')
#     user = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, verbose_name='担当スタッフ')
#     report_date = models.DateField('報告日', blank=True, null=True)
#     base_customer = models.ForeignKey(BaseCustomer, on_delete=models.CASCADE, verbose_name='オーナー顧客')
#     car_num = models.CharField('車両登録No.', max_length=100, blank=True, null=True)

#     def __str__(self):
#         return u'%s' % (self.report_date)

class Contact(models.Model):
    brand_id = models.IntegerField('ブランド販売店コード', blank=True, null=True)
    base_customer_id = models.CharField('顧客コード', max_length=100, blank=True, null=True)
    old_base_customer_id = models.CharField('旧顧客コード', max_length=100, blank=True, null=True)
    contact_date = models.DateField('接触日', blank=True, null=True)
    partner_kind = models.IntegerField('接触相手区分', blank=True, null=True)
    contact_way = models.IntegerField('接触方法', blank=True, null=True)
    shop = models.ForeignKey(Shop2, on_delete=models.SET_NULL, null=True, verbose_name='活動店舗')
    user = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, verbose_name='担当スタッフ')
    car_num = models.CharField('車両登録No.', max_length=100, blank=True, null=True)
    result_kind = models.CharField('活動結果コード', max_length=100, blank=True, null=True)

    def __str__(self):
        return u'%s' % (self.contact_date)

class Search(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, verbose_name='作成スタッフ')
    search_text = models.CharField('検索条件テキスト', max_length=255, blank=True)

    def __str__(self):
        return u'%s' % (self.search_text)

class Mylist2(TimestampedModel):
    title = models.CharField('タイトル', max_length=100, blank=False)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE) #User.model　リレーション
    customer_cars = models.ManyToManyField(CustomerCars, through='MylistCustomerCars') # Mylist-obj.customers.all()で取得可能、逆はCustomer-obj.mylist_set.all()で取得

    def __str__(self):
        return u'%s' % (self.title)

class MylistCustomerCars(models.Model):
    mylist = models.ForeignKey(Mylist2, on_delete=models.CASCADE)
    customer_cars = models.ForeignKey(CustomerCars, on_delete=models.CASCADE)
    done_flg = models.NullBooleanField('訪問チェック区分', null=True, blank=True)
    comment = models.CharField('コメント', max_length=100, blank=False, null=True)

class Schedule(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, verbose_name='対象社員')
    shop = models.ForeignKey(Shop2, on_delete=models.SET_NULL, null=True, verbose_name='活動店舗')
    registration_kind = models.IntegerField('発生元区分', blank=True, null=True)
    date = models.DateField('年月日', blank=True, null=True)
    from_time = models.IntegerField('時間から', blank=True, null=True) #I-CROPからのデータが数字なので数字として扱う
    to_time = models.IntegerField('時間まで', blank=True, null=True) #I-CROPからのデータが数字なので数字として扱う
    base_customer_id = models.CharField('顧客コード', max_length=100, blank=True, null=True) #スケジュールによっては顧客とのやり取りでないため空がある、よって明示的な外部キー宣言しない
    contact_way = models.IntegerField('接触方法', blank=True, null=True)
    activity_kind = models.IntegerField('活動項目区分', blank=True, null=True)
    car_num = models.CharField('車両登録No.', max_length=100, blank=True, null=True)

    def __str__(self):
        return u'%s' % (self.date)


#-------------GIS変更後DB--------------------------------------------------------
#変更前のDB使っているブランチはre_createまで
class GisCustomer(models.Model):
    class Meta:
        verbose_name_plural = '顧客車両データ'

    customer_code = models.CharField('顧客コード', max_length=100, blank=True, null=True)
    sex = models.IntegerField('性区分', blank=True, null=True)
    post_code = models.CharField('郵便番号', max_length=100, blank=True, null=True)
    address = models.CharField('住所', max_length=100, blank=True, null=True)
    lat = models.FloatField('緯度', blank=True, null=True)
    lng = models.FloatField('経度', blank=True, null=True)
    google_address = models.CharField('正規化住所', max_length=100, blank=True, null=True)
    location_rank = models.IntegerField('出力レベル', blank=True, null=True)
    partial_match = models.NullBooleanField('部分一致出力', null=True, blank=True)
    customer_fixed_kind = models.IntegerField('顧客固定客区分', blank=True, null=True)
    customer_rank = models.ForeignKey(Rank, on_delete=models.SET_NULL, related_name='customer_rank_set', null=True, verbose_name='顧客層別区分')
    car_num = models.CharField('車両No.', max_length=100, blank=True, null=True)
    # car = models.ForeignKey(Car, on_delete=models.SET_NULL, null=True, verbose_name='車両')
    car_model = models.CharField('車両型式', max_length=100, blank=True, null=True)
    car_name = models.CharField('車両名', max_length=100, blank=True, null=True)
    sale_flg = models.IntegerField('新中区分', null=True, blank=True)
    mini_flg = models.NullBooleanField('軽区分', null=True, blank=True)
    direct_kind = models.IntegerField('業直区分', blank=True, null=True)
    car_fixed_kind = models.IntegerField('車両固定客区分', blank=True, null=True)
    inspection_date = models.DateField('車検満了日', blank=True, null=True)
    insurance_date = models.DateField('保険満了日', blank=True, null=True)
    car_rank = models.ForeignKey(Rank, on_delete=models.SET_NULL, related_name='car_rank_set', null=True, verbose_name='車両層別区分')
    user = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, verbose_name='担当スタッフ')
    shop = models.ForeignKey(Shop2, on_delete=models.SET_NULL, related_name='shop_user_set', null=True, verbose_name='担当店舗')
    service_shop = models.ForeignKey(Shop2, on_delete=models.SET_NULL, related_name='service_shop_user_set', null=True, verbose_name='サービス担当店舗')
    csv_flg = models.BooleanField('CSV登録CK', default=False)

    def __str__(self):
        return u'%s' % (self.car_num)

class Department(models.Model):
    class Meta:
        verbose_name_plural = '業務マスタデータ'

    id = models.IntegerField('業務コード', primary_key=True)
    name = models.CharField('業務名', max_length=50, blank=True, null=True)
    auth_flg = models.BooleanField('商圏分析権限', default=False, help_text='ここをオンにすると、ユーザー画面でこの業務を持つユーザーが商圏分析機能にアクセスできます。')

    def __str__(self):
        return u'%s' % (self.name)
