from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'food'
urlpatterns = [
    path('', views.index, name='index'),
    path('user/<int:pk>/', views.users_detail, name='users_detail'),
    path('signup/', views.signup, name='signup'),
    path('shops/new/', views.shops_new, name='shops_new'),
    path('shops/<int:pk>/', views.shops_detail, name='shops_detail'), 
    path('shops/<int:pk>/edit/', views.shops_edit, name='shops_edit'),
    path('shops/<int:pk>/delete/', views.shops_delete, name='shops_delete'),
    path('login/', auth_views.LoginView.as_view(template_name='app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('search/', views.go_search, name='go_search'),    #必ずviewを経由しないと動かない？
    path('mylist_search/', views.go_mylist_search, name='go_mylist_search'),    #必ずviewを経由しないと動かない？
    path('mylist_search/result/', views.mylist_search, name='mylist_search'),
    path('search/result/', views.shops_search, name='shops_search'),  
    path('search/result/map', views.map_output, name='map_output'),  
    
]