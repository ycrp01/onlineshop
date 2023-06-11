from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from .forms import AddProductForm
from .cart import Cart
from coupon.forms import AddCouponForm

# Create your views here.
@require_POST # view가 POST만 허용하도록 하는 decorator.

# 제품 정보 전달 받으면 장바구니에 제품 추가. 제품 정보는 상세 페이지나 장바구니 페이지로부터 전달됨.
def add(request, product_id):
    cart = Cart(request) # 전달 받은 제품 객체를 cart 변수에 저장.
    product = get_object_or_404(Product, id=product_id) # cart에 저장된 제품의 procudt_id를 Product에서 찾아서 반환. 없으면 404 error

    form = AddProductForm(request.POST)

    if form.is_valid(): # form에 입력된 data를 검증하여 form에 입력되기 적절하면 cleaned_data 변수에 data를 대입.
        cd = form.cleaned_data # 즉, form에 입력되기 적절하다고 판명난 data를 cd 변수에 저장하는 것.
        cart.add(product=product, quantity=cd['quantity'], is_update=cd['is_update'])

    return redirect('cart:detail')

# 장바구니에서 제품 삭제.
def remove(request, product_id):
    cart = Cart(request) # 전달 받은 제품 객체를 cart 변수에 저장.
    product = get_object_or_404(Product, id=product_id) # cart에 저장된 제품의 procudt_id를 Product에서 찾아서 반환. 없으면 404 error
    cart.remove(product) #cart에서 product 삭제.

    return redirect('cart:detail')

# 장바구니 페이지.
def detail(request):
    cart = Cart(request)
    add_coupon = AddCouponForm()

    for product in cart:
        product['quantity_form'] = AddProductForm(initial={'quantity': product['quantity'], 'is_update': True})

    return render(request, 'cart/detail.html', {'cart': cart, 'add_coupon': add_coupon})
