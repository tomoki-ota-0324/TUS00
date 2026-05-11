from django.views.generic import View
from django.db.models import Q
from django.http.response import HttpResponse
from django.core import serializers

from sfacd.gis.models import Shop, Customer, Mylist
from sfacd.users.models import User
import geojson
import json
import datetime
from dateutil.relativedelta import relativedelta

class SearchCustomerView(View):

    def post(self, request, *args, **kwargs):
        print("view post")
        flg = False
        if request.POST['mylist'] == "true":
            flg = True

        if flg:
            print("サーバー側")
            rank_kinds = request.POST.getlist('rank_kinds')
            sale_kinds = request.POST.getlist('sale_kinds')
            inspection_limits = request.POST.getlist('inspection_limits')
            car_type = request.POST.getlist('car_type')
            shops = request.POST.getlist('shops')
            last_contact_date = [request.POST['last_contact_date_start'], request.POST['last_contact_date_end']]
            car_registration_date = [request.POST['car_registration_date_start'], request.POST['car_registration_date_end']]
        else:
            print("Ajax側")
            rank_kinds = request.POST.getlist('rank_kinds[]')
            sale_kinds = request.POST.getlist('sale_kinds[]')
            inspection_limits = request.POST.getlist('inspection_limits[]')
            car_type = request.POST.getlist('car_type[]')
            shops = request.POST.getlist('shops[]')
            last_contact_date = request.POST.getlist('last_contact_date[]')
            car_registration_date = request.POST.getlist('car_registration_date[]')

        #顧客層の絞り込み
        customers = Customer.objects.filter(staff_id=request.user.id) #ログインユーザーの担当顧客の中から
        if len(rank_kinds) > 0:
            customers = self.refine_record(customers, rank_kinds, 'rank_kind')
        
        #販売区分の絞り込み
        if len(sale_kinds) > 0:
            customers = self.refine_record(customers, sale_kinds, 'sale_kind')

        #車種の絞り込み
        if len(car_type) > 0:
            customers = self.refine_record(customers, car_type, 'car_type')

        #店舗の絞り込み
        if len(shops) > 0:
            customers = self.refine_record(customers, shops, 'staff_shop_id')

        kwargs = {}
        today = datetime.date.today()

        #車検の絞り込み
        for month in inspection_limits:
            from_date = today + relativedelta(months=int(month)) #注意：未来 小さい
            to_date = from_date + relativedelta(months=3) #大きい
            kwargs['inspection_date__gte'] = from_date
            kwargs['inspection_date__lt'] = to_date

        #最終接触
        to_date = today - relativedelta(months=int(last_contact_date[0])) #注意：過去 大きい
        from_date = today - relativedelta(months=int(last_contact_date[1])) #小さい
        if int(last_contact_date[0]) != 0:
            kwargs['last_contact_date__gte'] = from_date
        if int(last_contact_date[1]) != 0:
            kwargs['last_contact_date__lt'] = to_date

        #初回登録
        to_date = today - relativedelta(years=int(car_registration_date[0])) #注意：過去 大きい
        from_date = today - relativedelta(years=int(car_registration_date[1])) #小さい
        if int(car_registration_date[0]) != 0:
            kwargs['car_registration_date__gte'] = from_date
        if int(car_registration_date[1]) != 0:
            kwargs['car_registration_date__lt'] = to_date

        customers = customers.filter(**kwargs)

        if flg:
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


