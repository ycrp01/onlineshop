from django.shortcuts import render
from django.shortcuts import redirect
from django.utils import timezone
from django.views.decorators.http import require_POST

from .models import Coupon
from .forms import AddCouponForm


# Create your views here.
@require_POST # view가 POST request만 받도록 함.
def add_coupon(request):
    now = timezone.now()
    form = AddCouponForm(request.POST) # request된 데이터 form에 대입.
    if form.is_valid(): # form의 적절성 검사.
        code = form.cleaned_data['code'] # 입력한 쿠폰 코드 조회.
        try:
            coupon = Coupon.objects.get(code__iexact=code, use_from__lte=now, use_to__gte=now, active=True) # iexact: 대소문자 구분 없이 검색.
            request.session['coupon_id'] = coupon.id

        except Coupon.DoesNotExist:
            request.session['coupon_id'] = None

    return redirect('cart:detail')