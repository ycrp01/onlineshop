from django.contrib import admin
from .models import *

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug':('name',)} # slug field를 name field 값에 따라 자동으로 설정.

class ProductAdmin(admin.ModelAdmin):
    list_display=['name', 'slug', 'category', 'price', 'stock', 'available_display', 'available_order', 'created', 'updated']
    prepopulated_fields = {'slug': ('name',)} # slug field를 name field 값에 따라 자동으로 설정.
    list_editable =['price', 'stock', 'available_display', 'available_order'] # 목록에서 주요 값들 바로 변경 가능.

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)