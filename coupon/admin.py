from django.contrib import admin
from .models import Coupon

# Register your models here.
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'use_from', 'use_to', 'amount', 'active'] # active 체크해야 쿠폰 사용 가능
    list_filter = ['active', 'use_from', 'use_to'] # active 체크해야 쿠폰 사용 가능
    search_fields = ['code']

admin.site.register(Coupon, CouponAdmin)