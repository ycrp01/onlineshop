from django.urls import path
from .views import *

app_name = 'shop'

urlpatterns = [
    path('', product_in_category, name='product_all'), # category 선택 없을 때
    path('<category_slug>/', product_in_category, name='product_in_category'), # category 선택 있을 때
    path('<int:id>/<product_slug>/', product_detail, name='product_detail'), # 제품 상세 내역
]