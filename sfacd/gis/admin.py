from django.contrib import admin
from sfacd.gis.models import Shop2, GisCustomer, Rank, Department, Shop2Detail


class Shop2DetailInline(admin.StackedInline):
    model = Shop2Detail

class Shop2Admin(admin.ModelAdmin):
    list_display = ['id', 'name', 'new_flg', 'ucar_flg', 'service_flg', 'brand_id', 'shop_flg', 'shop_kind_name']
    list_filter = ['new_flg', 'ucar_flg', 'service_flg', 'shop_flg', 'shop_kind']
    ordering = ['id']
    inlines = [Shop2DetailInline]

    #外部キーに紐づく値を表示。Shop2テーブルのshop_name
    def shop_kind_name(self, obj):
        if obj.shop_kind == 1:
            # return 'トヨペット'
            return 'トヨタユナイテッド静岡' # 2022/11/3 管理画面の表の名称変更
        elif obj.shop_kind == 2:
            return 'カローラ東海'
        elif obj.shop_kind == 3:
            return 'ネッツスルガ'
        elif obj.shop_kind == 4:
            return '候補地地点'
        else:
            return '不明'
    shop_kind_name.short_description = '店舗種別' #画面のカラム名

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'auth_flg']
    list_filter = ['auth_flg']
    ordering = ['id']

class RankAdmin(admin.ModelAdmin):
    list_display = ['rank']
    ordering = ['id']

class GisCustomerAdmin(admin.ModelAdmin):
    list_display = ['customer_code', 'car_num', 'customer_rank', 'car_rank', 'user', 'shop', 'service_shop']
    # ordering = ['id']
    list_filter = ['sale_flg', 'customer_rank', 'car_rank']


# Register your models here.
admin.site.register(GisCustomer, GisCustomerAdmin)
# admin.site.register(Shop2, ExtendedShop2Admin)
admin.site.register(Shop2, Shop2Admin)
admin.site.register(Rank, RankAdmin)
admin.site.register(Department, DepartmentAdmin)

admin.site.site_title = '商圏分析ツール 管理サイト'
admin.site.site_header = '商圏分析ツール'
admin.site.index_title = 'メニュー'
