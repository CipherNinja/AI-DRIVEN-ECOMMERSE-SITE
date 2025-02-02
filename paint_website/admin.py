from django.contrib import admin
from .models import *


@admin.register(Our_Product)
class DocumentModelAdmin(admin.ModelAdmin):
    list_display = ["id","product_image","product_name","product_detail","product_price"]

@admin.register(Top_Product)
class DocumentModelAdmin(admin.ModelAdmin):
    list_display = ["id","product_image","product_name","product_detail","product_price"]

@admin.register(Blog_Event)
class DocumentModelAdmin(admin.ModelAdmin):
    list_display = ["id","blog_image","blog_name","blog_detail","blog_date"]


@admin.register(UserInfo)
class DocumentModelAdmin(admin.ModelAdmin):
    list_display = ["id","user","address","phone_number"]

@admin.register(AllOrderDetail)
class DocumentModelAdmin(admin.ModelAdmin):
    list_display = ["id","user","product","quantity","delivery_date","order_date"]

@admin.register(ShoppingCart)
class DocumentModelAdmin(admin.ModelAdmin):
    list_display = ["id","user","product","quantity","price"]

