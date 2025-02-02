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
    path("logout/",views.Logout_User,name="logout"),
]
