from django.views.generic import View
from django.db.models import Q
from django.http.response import HttpResponse
from django.core import serializers

from sfacd.gis.models import Shop2, GisCustomer
from sfacd.users.models import User
import geojson
import json


class GetEachStaffListView(View):

    def post(self, request, *args, **kwargs):
        shops = request.POST.getlist('shops[]')

        if len(shops) > 0:
            # アクティブ状態の従業員かつ、選択された店舗に紐づく従業員、担当車両を持たない従業員も選択肢にいる
            # もし店舗の持つ顧客車両数と紐づく従業員別に表示する場合は、店舗のみ選択した状態で、マーカーカラー変更リストで従業員別を選択する
            staffs = User.objects.filter(is_active=True, shop_id__in=shops).order_by('-id')
        else:
            staffs = []
        # print(staffs.query)

        # 選択された店舗と紐ずく車両を担当している従業員を全員抽出するので、従業員の所属が必ずしも選択された店舗ではない、ただ店舗で絞り込んだ車両数と従業員を全員選択した車両数が一致する
        # users_ids_list = GisCustomer.objects.filter(user__is_active=True, shop_id__in=shops).values_list('user_id', flat=True).distinct()
        # print(len(users_ids_list))
        # staffs = User.objects.filter(id__in=users_ids_list).order_by('id')
        # print(staffs.query)

        qs_json = serializers.serialize('json', staffs)
        # print(qs_json)
        return HttpResponse(qs_json, content_type='application/json')

