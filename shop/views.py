from django.shortcuts import render, get_object_or_404
from .models import *

# Create your views here.
def product_in_category(request, category_slug=None):
    # 변수 정의
    current_category = None
    categories = Category.objects.all() # Category model의 모든 데이터 categories 변수에 저장.
    products = Product.objects.filter(available_display=True) # Product model 중 노출 가능한 상품만 products 변수에 저장.

    # URL로부터 category_slug 찾아서 그 category 노출. category 없으면 상품 전체 목록 노출.
    if category_slug:
        current_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=current_category)

    return render(request, 'shop/list.html', {'current_category': current_category, 'categories': categories, 'products': products})

from cart.forms import AddProductForm # 장바구니 담기 기능을 위해 필요.

def product_detail(request, id, product_slug=None):
    product = get_object_or_404(Product, id=id, slug=product_slug)
    add_to_cart = AddProductForm(initial={'quantity': 1})
    return render(request, 'shop/detail.html', {'product': product, 'add_to_cart': add_to_cart})

