from django import forms

from sfacd.gis.models import GisCustomer

class CreateCustomerForm(forms.ModelForm):
    """
    現在不使用中
    """
    class Meta:
        model = GisCustomer #モデル指定
        fields = "__all__" #表示フィールドを指定

    #追加フィールドあれば

    def clean_giscustomer(self):
        """
        バリデーション
        """