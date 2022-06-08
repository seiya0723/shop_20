from django.urls import path
from . import views

app_name    = "shop"
urlpatterns = [
    path('', views.index, name="index"),
    path('<uuid:pk>/', views.product, name="product"), #商品のID
    path('<uuid:pk>/comment/', views.product_comment, name="product_comment"), #商品のID
    path('cart/', views.cart, name="cart"),
    path('cart/<uuid:pk>/', views.cart, name="cart_single"), #カートのID


    path('ranking/', views.ranking, name="ranking"),

    path('address/', views.address, name="address"),
    path('checkout_before/', views.checkout_before, name="checkout_before"),
    

    #このpkはOrderモデルのid
    path('checkout/<uuid:pk>/', views.checkout, name="checkout"),
    path('checkout_success/<uuid:pk>/', views.checkout_success, name="checkout_success"),
    path('checkout_error/', views.checkout_error, name="checkout_error"),


    path('order_history/', views.order_history, name="order_history"),


    #TODO:ここで売上のデータ確認
    path('analyse/', views.analyse, name="analyse"),


    #TODO:ここで閲覧履歴
    path('history/', views.history, name="history"),



]

