from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponse
from django.views.generic import TemplateView
from django.db.models import Q
from django.core import serializers

from sfacd.gis.models import Shop2, Rank, Car, Activity, ContactPartner, ContactWay, ContactResult, CustomerCars
from sfacd.gis.views.Constant import Constant
import geojson
import json
import datetime
from dateutil.relativedelta import relativedelta
# Python 3.13対応：distutils廃止のため自前定義
def strtobool(val):
    val = str(val).lower()
    if val in ('y', 'yes', 't', 'true', 'on', '1'):
        return 1
    elif val in ('n', 'no', 'f', 'false', 'off', '0'):
        return 0
    else:
        raise ValueError(f"invalid truth value {val!r}")

class MainMapView(LoginRequiredMixin, TemplateView):
    template_name = "gis/main_map.html"

    def get(self, request, *args, **kwargs):
        """
        メインマップのダイレクト表示処理
        """
        print("初回表示")
        brand_id = Shop2.objects.get(id=request.user.shop_id).brand_id
        activities = Activity.objects.filter(brand_id=brand_id)
        partners = ContactPartner.objects.filter(brand_id=brand_id)
        contactways = ContactWay.objects.filter(brand_id=brand_id)
        ranks = Rank.objects.all()
        cars = list(Car.objects.all().values_list('name', flat=True).order_by('name').distinct())
        current_shop = Shop2.objects.get(id=request.user.shop_id)
        context = super().get_context_data(
            api_key=Constant().FRONT_API,
            current_shop=current_shop,
            ranks=ranks,
            cars=cars,
            activities=activities,
            partners=partners,
            contactways=contactways,
            refine_flg=False, #GETでダイレクトアクセスされると自分の顧客が見ている範囲分表示される、絞込なしを判定
        )
        return super().render_to_response(context)

    def post(self, request, *args, **kwargs):
        print("絞込Ajax")
        refine_flg = request.POST['refine_flg']
        base_customer_rank = request.POST.getlist('base_customer_rank[]')
        base_customer_sex = request.POST.getlist('base_customer_sex[]')
        fixed_kind = request.POST.getlist('fixed_kind[]')
        sale_flg = request.POST.getlist('sale_flg[]')
        customer_cars_rank = request.POST.getlist('customer_cars_rank[]')
        car = request.POST.getlist('car[]')
        registration_date = request.POST.getlist('registration_date[]')
        ucar_registration_date = request.POST.getlist('ucar_registration_date[]')
        inspection_date = request.POST.getlist('inspection_date[]')
        limit_date = request.POST.getlist('limit_date[]')
        contact_date = request.POST.getlist('contact_date[]')
        
        #顧客層の絞り込み
        customers = CustomerCars.objects.filter(user_id=request.user.id).select_related() #ログインユーザーの担当顧客の中から
        if len(base_customer_rank) > 0:
            customers = self.refine_record(customers, base_customer_rank, 'base_customer__rank__id')
        
        #性別区分の絞り込み
        if len(base_customer_sex) > 0:
            customers = self.refine_record(customers, base_customer_sex, 'base_customer__sex')

        #固定客の絞り込み
        if len(fixed_kind) > 0:
            customers = self.refine_record(customers, fixed_kind, 'fixed_kind')

        #新中の絞り込み
        if len(sale_flg) > 0:
            customers = self.refine_record(customers, sale_flg, 'sale_flg')

        #車両層の絞り込み
        if len(customer_cars_rank) > 0:
            customers = self.refine_record(customers, customer_cars_rank, 'rank__id')

        #車名の絞り込み
        if len(car) > 0:
            customers = self.refine_record(customers, car, 'car__name__icontains')
            
        kwargs = {}
        today = datetime.date.today()

        #初回登録
        to_date = today - relativedelta(years=int(registration_date[0])) #注意：過去 大きい
        from_date = today - relativedelta(years=int(registration_date[1])) #小さい
        if int(registration_date[0]) != 0:
            kwargs['registraction_date__gte'] = from_date
        if int(registration_date[1]) != 0:
            kwargs['registraction_date__lt'] = to_date

        #U-Car登録
        to_date = today - relativedelta(years=int(ucar_registration_date[0])) #注意：過去 大きい
        from_date = today - relativedelta(years=int(ucar_registration_date[1])) #小さい
        if int(ucar_registration_date[0]) != 0:
            kwargs['ucar_registraction_date__gte'] = from_date
        if int(ucar_registration_date[1]) != 0:
            kwargs['ucar_registraction_date__lt'] = to_date

        #車検満了日期間
        from_date = today + relativedelta(months=int(inspection_date[0])) #注意：未来 小さい
        to_date = today + relativedelta(months=int(inspection_date[1])) # 大きい
        if int(inspection_date[0]) != 0:
            kwargs['inspection_date__gte'] = from_date
        if int(inspection_date[1]) != 0:
            kwargs['inspection_date__lt'] = to_date

        #活動期限
        # to_date = today - relativedelta(months=int(limit_date[0])) #注意：過去 大きい
        # from_date = today - relativedelta(months=int(limit_date[1])) #小さい
        # if int(limit_date[0]) != 0:
        #     kwargs['limit_date__gte'] = from_date
        # if int(limit_date[1]) != 0:
        #     kwargs['limit_date__lt'] = to_date

        #接触日
        # to_date = today - relativedelta(months=int(contact_date[0])) #注意：過去 大きい
        # from_date = today - relativedelta(months=int(contact_date[1])) #小さい
        # if int(contact_date[0]) != 0:
        #     kwargs['contact_date__gte'] = from_date
        # if int(contact_date[1]) != 0:
        #     kwargs['contact_date__lt'] = to_date

        customers = customers.filter(**kwargs).order_by('id')

        if strtobool(refine_flg): #もし検索条件が設定されているなら
            print('検索の設定あり')
            return customers
        else:
            customers_ids = list(customers.values('id'))
            print(len(customers))
            print(customers.query)

            data = {
                'len': len(customers),
                'customers_ids': customers_ids
            }
            data = json.dumps(data)
            return HttpResponse(data, content_type='application/json')


    def refine_record(self, obj, lst, column_name):
        """
        obj: モデルオブジェクト
        lst: 同一カラム内の絞込要素、要素は文字列
        column_name：絞込をする対象カラム
        """
        q1 = []
        query1 = []

        for l in lst:
            q = Q()
            q.children.append((column_name, l))
            q1.append(q)

        if len(q1) != 0:
            query1 = q1.pop()
            for item in q1:
                query1 |= item
        refine_obj = obj.filter(query1)
        print(len(refine_obj))
        return refine_obj


