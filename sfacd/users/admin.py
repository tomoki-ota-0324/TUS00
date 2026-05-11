from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model

from sfacd.users.forms import UserChangeForm, UserCreationForm

User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (("User", {"fields": ("name",)}),) + auth_admin.UserAdmin.fieldsets
    list_display = ["id", "name", "email", "shop_name", "department_name", "is_staff", "is_active"] #表示一覧画面に見せるもの
    search_fields = ["id", "name", "email", "shop__name", "department__name"] #入力検索の条件にかかるもの
    list_filter = ['is_staff', 'is_active', 'department__auth_flg'] #表示一覧画面の右側フィルターに表示するもの

    #追加情報画面の項目
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('従業員情報', {'fields': ('id', 'shop', 'name')}),
        ('操作権限', {'fields': ('department', 'is_active', 'is_staff', 'groups')}),
        ('更新日付', {'fields': ('date_joined',)}),
    )

    #ユーザ追加画面に登録項目追加
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('id', 'password1', 'password2', 'name', 'email', 'shop', 'department'),
        }),
    )

    #外部キーに紐づく値を表示。Shop2テーブルのshop_name
    def shop_name(self, obj):
        if obj.shop is None:
            return 'なし'
        else:
            return obj.shop.name
    shop_name.short_description = '所属店舗' #画面のカラム名

    def department_name(self, obj):
        if obj.department is None:
            return 'なし'
        else:
            return obj.department.name
    department_name.short_description = '業務グループ'
