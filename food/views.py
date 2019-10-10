from django.shortcuts import get_object_or_404, redirect, render
from .models import Shop
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from .forms import ShopForm
from .forms import SearchForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST

import requests
import urllib
from bs4 import BeautifulSoup
# import pandas as pd
import re
# import numpy as np
import time
from tqdm import tqdm
import folium
import base64

def index(request):
    shops = Shop.objects.all().order_by('-id')
    return render(request, 'app/index.html', {'shops': shops})

def users_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    return render(request, 'app/users_detail.html', {'user': user})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST) # ユーザーインスタンスを作成
        if form.is_valid():
            new_user = form.save() # ユーザーインスタンスを保存
            input_username = form.cleaned_data['username']
            input_password = form.cleaned_data['password1']
            # フォームの入力値で認証できればユーザーオブジェクト、できなければNoneを返す
            new_user = authenticate(username=input_username, password=input_password)
            # 認証成功時のみ、ユーザーをログインさせる
            if new_user is not None:
                # loginメソッドは、認証ができてなくてもログインさせることができる。→上のauthenticateで認証を実行する
                login(request, new_user)
                return redirect('app:index.html', pk=new_user.pk)
    else:
        form = UserCreationForm()
    return render(request, 'app/signup.html', {'form': form})
    
    
    
@login_required  
def shops_new(request):
    if request.method == "POST":
        form = ShopForm(request.POST, request.FILES)
        if form.is_valid():
            shop = form.save(commit=False)
            # photo = request.FILES['pic']
            # data = photo.read()
            # photo_binary=base64.b64encode(data)
            # shop.photo_binary = photo_binary
            # base64.b64encode(data)
            shop.user = request.user
            shop.save()      
            messages.success(request, "登録が完了しました！")                
#    return redirect('app:users_detail', pk=request.user.pk)
        return render(request,'app/success.html')
    else:
        form = ShopForm()
    return render(request, 'app/shops_new.html', {'form': form})

def go_search(request):    
#    form = SearchForm()
#    return render(request, 'app/shops_search.html', {'form': form})
    return render(request, 'app/shops_search.html')

def go_mylist_search(request):
    form = SearchForm  
    return render(request, 'app/mylist_search.html',{'form':form})



def mylist_search(request):  
    form =SearchForm(request.GET)
    if form.is_valid(): #フォームの値をチェックしないと下がエラーになる
        name=form.cleaned_data.get('name')
        station=form.cleaned_data.get('station')    #データを整型して返す
        genre=form.cleaned_data.get('genre')
        shops ={}
        #DBへのアクセスはクエリが確定したとき
        if name :    #空でないとき
            shops = Shop.objects.filter(name__icontains=name)  #_は２つ！
        if station :    #空でないとき
            shops = Shop.objects.filter(station__icontains=station)            
        if genre   :
            shops = Shop.objects.filter(genre__icontains=genre)   
        if shops :   #検索結果が空かどうかの判断 
            messages.success(request, str(len(shops)) +"件が見つかりました！")  #messageはsuccessのみ？ 
            try:
                #セッションに検索結果を保存
                if 'search_result' in request.session:
                    del request.session['search_result']
                request.session['search_result'] = shops
                print('セッション格納成功')
                print(len(request.session['search_result']))    
            except:
                print('セッション格納エラー')
            return render(request, 'app/search_result.html', {'shops': shops})
        else:       #空のモデルを返すとエラーになる
            messages.success(request, "該当する結果がありませんでした・・・")  #messageはsuccessのみ？               
            return render(request, 'app/search_result.html')



def shops_detail(request, pk):
    shop = get_object_or_404(Shop, pk=pk)
    return render(request, 'app/shops_detail.html', {'shop': shop})

@require_POST
def shops_delete(request, pk):
    shop = get_object_or_404(Shop, pk=pk)
    shop.delete()
    messages.success(request, "削除が完了しました！")                
    return render(request,'app/success.html')
    
def shops_edit(request, pk):
    shop = get_object_or_404(Shop, pk=pk)
    if request.method == "POST":
        form = ShopForm(request.POST,request.FILES,instance=shop)
        if form.is_valid():
            form.save()
            messages.success(request, "編集が完了しました！")                
            print("編集終了 ID=" + str(pk) )
        return render(request,'app/success.html')    
    else:
        print("編集開始 ID=" + str(pk) )
        print(shop.name) 
        form = ShopForm(instance=shop)
    return render(request,'app/shops_edit.html', {'form': form,'shop':shop})   
def map_output(request):
    print('セッション情報取得')
    # shops = request.session.get('search_result'
    shops = request.session['search_result']
    
    print('マップ定義')
    # map = folium.Map(location=[35.002408,135.759718], zoom_start=15)
    i = 0
    j = 0
    for shop in shops:

        try:
                
                print(shop.name)
                work_coord = shop.coordinate.split(",")
                lat =float(work_coord[0])
                print(lat)
                lon =float(work_coord[1])
                print(lon)
        #         latlons.append([lat,lon])
                if i == 0 :
                    map = folium.Map(location=[lat,lon], zoom_start=15)
                html_link='<a href="'+shop.url+'" target="_blank">お店の詳細を見る</a>'
                print(html_link)
                # popup='評価：'+str(shop.evaluate) + '<br />'+str(shop.name)+ '<br />'+str(shop.genre) +'<br />'+'昼：'+ str(shop.lunch_bud) + '<br />'+'夜：' + str(shop.dinner_bud) + '<br />' +str(html_link)
                # popup='<nobr>評価：'+str(shop.evaluate) + '</nobr><br><nobr>'+str(shop.name)+ '</nobr><br><nobr>'+str(shop.genre) +'</nobr><br><nobr>'+'昼：'+ str(shop.lunch_bud) + '</nobr><br><nobr>'+'夜：' + str(shop.dinner_bud) + '</nobr><br><nobr>' +str(html_link)
                popup='<div style="white-space:nowrap;">評価：'+str(shop.evaluate) + '<br>'+str(shop.name)+ '<br>'+str(shop.genre) +'<br>'+'昼：'+ str(shop.lunch_bud) + '<br>'+'夜：' + str(shop.dinner_bud) + '</div>'
                
                
                if shop.evaluate >= 3.5 :
                    icon_color="red"
                elif shop.evaluate >= 3.3:
                    icon_color="orange"
                else: 
                    icon_color="blue"
                print('プロット開始')
                # marker = folium.Marker([ lat,lon ], popup=popup,icon=folium.Icon(color=icon_color))
                marker = folium.Marker([ lat,lon ], popup=popup,icon=folium.Icon(color=icon_color))
                map.add_child(marker)
                print('プロット完了')
                i = i + 1
        except:
            j = j + 1  #エラー件数
            print('取得エラー') 
    print('取得エラー '+ str(j) )                  
    map.save('app/templates/app/map.html')
    return render(request,'app/map.html') 
def shops_search(request):
    i = 0
    address =""
    evaluate =""
    kuchikomi =""
    teikyu =""
    lunch_bud =""
    dinner_bud =""
    info =[]
    name =""
    geourl = 'http://www.geocoding.jp/api/'

    
    # URLから店名、住所、最寄り駅、ジャンル、評価、口コミ数、定休日、昼予算、夜予算を取得
#    url = 'https://tabelog.com/okayama/A3301/A330101/33001614/'

    url=request.GET.get('search_url')    
#    form=SearchForm(request.GET)
#    url =form.url
#    form_obj = form.save(commit=False)    
#    url=form_obj.url
    
    
    html = urllib.request.urlopen(url)
    soup = BeautifulSoup(html, "html.parser")


    name=soup.find(class_="display-name").getText().strip()  #strip で不要な空白を削除

    for info in soup.findAll("span",class_="linktree__parent-target-text"):
        i= i + 1
        if i == 1 :   #駅名
            station = re.split('駅',info.getText())[0]
        if i == 3 :   #1つ目のジャンル
            genre = info.getText()
        if i >3   :   #2つ目以降のジャンル
            genre = genre + "、" + info.getText()
        
    try:
        address=soup.find("p",class_="rstinfo-table__address").getText()
    except:
        address="住所情報なし"
    try:    
        evaluate=soup.find(class_="rdheader-rating__score-val-dtl").getText()
    except:
        evaluate=0
    try:    
        kuchikomi=soup.find(class_="num").getText()
    except:
        kuchikomi=0 
    try:    
        teikyu=soup.find(class_="rdheader-subinfo__closed-text").getText().strip()
    except :
        teikyu="定休情報なし"
    try:    
        lunch_bud=soup.find(class_="gly-b-lunch").getText()
    except:
        lunch_bud="ランチ情報なし"    
    try:
        dinner_bud=soup.find(class_="gly-b-dinner").getText()
    except :
        dinner_bud="ディナー情報なし"
 #  googleのAPIを利用し、住所を緯度経度に変換する。　
    payload = {'q': address}
    r = requests.get(geourl, params=payload)
    ret = BeautifulSoup(r.content,'lxml')
    if ret.find('error'):
        raise ValueError(f"Invalid address submitted. {address}")
    else:
 #  緯度経度の取得に成功したときの処理  
        lat =float(ret.find('lat').string)
        lon =float(ret.find('lng').string) 	
        
#    shop = get_object_or_404(Shop, pk=1)

#    shop=Shop.objects.create(
#    name = name,
#    evaluate=evaluate,
#    station=station,
#    genre=genre,
#    url =url,
#    coordinate=str(lat)+ "," + str(lon),
#    user =request.user,
#    )

#    shop = create(Shop)    

    shop=Shop       
    shop.name = name
    shop.evaluate=evaluate
    shop.station=station
    shop.genre=genre
    shop.url =url
    shop.coordinate=str(lat)+ "," + str(lon)
    shop.comment=""
    shop.kuchikomi=kuchikomi
    shop.teikyu=teikyu
    shop.lunch_bud=lunch_bud
    shop.dinner_bud=dinner_bud
    shop.user =request.user
    
    print("【URL検索_実行結果】")
    print(shop.name)
    print(shop.evaluate)
    print(shop.station)
    print(shop.genre)
    print(shop.url)
    print(shop.coordinate)
    
#    initial_dict = {
#        'name' : name,
#        'evaluate' : evaluate
#    }
#     initial_dict= {
#     'name' : name,
#     'evaluatea :evaluate'
#     }
#    form = ShopForm(request.POST or None, initial = shop)
 #   return render(request, 'app/shops_new.html', {'shop': shop})
    
    form =ShopForm(instance=shop)

#    form.name=name
#    return render(request, 'app/search_result.html', {'shop': shop})
    return render(request, 'app/shops_new.html', {'form': form})
    
    
    
 
                