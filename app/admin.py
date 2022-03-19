from django.contrib import admin
from  .models import (Customer,ProductDetail,Cart,ProductPlaced)
# Register your models here.

@admin.register(Customer)
class CustomerModleAdmin(admin.ModelAdmin):
    list_display=['id','user','name','locality','city','state','zipcode']

@admin.register(ProductDetail)
class ProductModleAdmin(admin.ModelAdmin):
    list_display=['id','title','selling_price','discount_price','descripttion','brand','category','product_image']

@admin.register(Cart)
class CartModleAdmin(admin.ModelAdmin):
    list_display=['id','user','product','quantity']

@admin.register(ProductPlaced)
class ProductPlacedModleAdmin(admin.ModelAdmin):
    list_display=['id','user','customer','product','quantity','order_date','status']