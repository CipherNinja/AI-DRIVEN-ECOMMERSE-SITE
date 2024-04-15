from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    
    path("",views.home_page_register_view,name="home"),
    path("login/",views.home_page_login_view,name="login_matching"),
    path("contact/",views.Contactus_View,name="contact"),
    path("developer/",views.Developer_View,name="developer"),
    path("staff/",views.Staff_Login_View,name="staff"),
    path("products/",views.Product_View,name="products"),
    path("update/",views.home_page_update_view,name="update"),
    path("login_required/",views.Login_required_mixin,name="login_required"),
    path("cart/",views.My_Cart_View,name="cart"),
    path("purchase-all/",views.My_Cart_View_Purchase_All,name="purchase_items"),
    path("we-are-gniotians/",views.Give_credits,name="we-are-gniotians"),
    path("we-are-gniotians/sahil/",views.Free_Credit_To_Sahil,name="we-are-gniotians-sahil-chaubey"),
    path("we-are-gniotians/Iswar-Singh/",views.Ishwar_Singh,name="we-are-gniotians-Ishwar-Singh"),
    path("we-are-gniotians/Deepak-sir/",views.Deepak_sir_it,name="we-are-gniotians-Deepak-sir"),
    path("we-are-gniotians/Vijay-Sukla/",views.Hod_sir_it,name="we-are-gniotians-vijay"),
    path("logout/",views.Logout_User,name="logout"),
    path("myorder/",views.Order_Tracking_Sytem,name="myorder"),
     path('high-demand-products/', views.high_demand_products_view, name='high_demand_products'),
    path("alldata/",views.predict_all_users_view,name="predict_all"),

]
