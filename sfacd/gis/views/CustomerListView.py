from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from sfacd.gis.models import Shop, Customer, Shop2, BaseCustomer, CustomerCars
from sfacd.gis.views.CreateMainMapMarkerView import CreateMainMapMarkerView
from django.db.models import Q

import datetime


class CustomerListView(LoginRequiredMixin, TemplateView):
    template_name = "gis/customer_list.html"

    def get(self, request, *args, **kwargs):
        customers = CustomerCars.objects.filter(user_id=request.user.id).select_related().prefetch_related()
        context = super().get_context_data(
            customers=customers,
        )
        return super().render_to_response(context)

    def post(self, request, *args, **kwargs):
        customers, shops = CreateMainMapMarkerView().get_customers(request)
        # print(customers)

        context = super().get_context_data(
            customers=customers,
        )
        return super().render_to_response(context)
        

        # submit = request.POST['mylist']
        # if submit == 'search':
        #     title = request.POST['title'] #リスト名

        #     rank_kinds = request.POST.getlist('rank_kind') #顧客層 ALL, SS, A etc..

        #     sale_kinds = request.POST.getlist('sale_kind') #販売区分 0：すべて 1:新車, 2:中古

        #     inspection_limit = request.POST['inspectionRadioz'] #車検満期期間 0, 3, 6, 9
        #     car_type = request.POST.getlist('car_type') #車種 'アルファード' etc..

        #     shops = request.POST.getlist('shops') #店舗 id

        #     start_date = request.POST['last_contact_date1'] #最終接触期間 '01/01/2019' start date
        #     last_contact_date1 = self.str_to_date(start_date)
        #     end_date = request.POST['last_contact_date2'] #最終接触期間 '01/01/2019' end date
        #     last_contact_date2 = self.str_to_date(end_date)

        #     start_date = request.POST['car_registration_date1'] #初回登録期間 '01/01/2019' start date
        #     car_registration_date1 = self.str_to_date(start_date)
        #     end_date = request.POST['car_registration_date2'] #初回登録期間 '01/01/2019' end date
        #     car_registration_date2 = self.str_to_date(end_date)

        #     if not last_contact_date1 < last_contact_date2:
        #         raise ValueError("最終訪問日の設定期間が間違っています")
        #     if not car_registration_date1 < car_registration_date2:
        #         raise ValueError("初回登録日の設定期間が間違っています")
            
        #     today = datetime.date.today()
        #     inspection_limit_date = today + relativedelta(months=int(inspection_limit))

        #     #顧客層の絞り込み
        #     obj = Customer.objects
        #     customers = self.refine_record(obj, rank_kinds, 'rank_kind')

        #     #販売区分の絞り込み
        #     customers = self.refine_record(customers, sale_kinds, 'sale_kind')

        #     #車種の絞り込み
        #     customers = self.refine_record(customers, car_type, 'car_type')

        #     #店舗の絞り込み
        #     customers = self.refine_record(customers, shops, 'staff_shop_id')

        #     print(len(customers))

        #     #車検満期、最終接触、初回登録
        #     kwargs = {
        #         '{0}__{1}'.format('inspection_date', 'gte'): today,
        #         '{0}__{1}'.format('inspection_date', 'lte'): inspection_limit_date,
        #         '{0}__{1}'.format('last_contact_date', 'gte'): last_contact_date1,
        #         '{0}__{1}'.format('last_contact_date', 'lte'): last_contact_date2,
        #         '{0}__{1}'.format('car_registration_date', 'gte'): car_registration_date1,
        #         '{0}__{1}'.format('car_registration_date', 'lte'): car_registration_date2,
        #     }
        #     customers = customers.filter(**kwargs)

        #     print(len(customers))
        #     print(customers)

        #     context = self.get_context_data()
        #     context['customers'] = customers
        #     context['title'] = title
        #     return super().render_to_response(context)

        # elif submit == 'save':
        #     customer_ids = request.POST.getlist('customer_ids') #リストを生成するための顧客のidの入ったリスト
        #     title = request.POST['title'] #リストのタイトル

        #     mylist = Mylist()
        #     print(mylist)
        
    def str_to_date(self, strdate):
        """
        '12/01/2018'の順序のテキスト日付をdatetime.date型に変換しreturnする
        """
        tdatetime = datetime.datetime.strptime(strdate, '%m/%d/%Y')
        tdate = datetime.date(tdatetime.year, tdatetime.month, tdatetime.day)
        return tdate

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

