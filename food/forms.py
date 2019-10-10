from django.forms import ModelForm
from django import forms
from .models import Shop


class ShopForm(ModelForm):
    class Meta:
        model = Shop
        fields = ['name', 'evaluate', 'station', 'genre','url','coordinate','state','comment','kuchikomi','teikyu','lunch_bud','dinner_bud']

#検索用のフォーム
class SearchForm(forms.Form):
    name=forms.CharField(label='店名', required=False)
    station=forms.CharField(label='駅', required=False)
    genre=forms.CharField(label='ジャンル', required=False)

        
#フォームでクラス定義⇒単純にgetメソッドを採用        
#class SearchForm(forms.Form):
#    url=forms.CharField()