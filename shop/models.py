from django.db import models
from django.urls import reverse

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True) # category 이름
    meta_description = models.TextField(blank=True) # SEO(Search Engine Optimization) 목적. 검색에 이용.

    slug = models.SlugField(max_length=200, db_index=True, allow_unicode=True) # 상품명 등 이용해서 URL 만드는 방식.

    class Meta:
        ordering = ['name']
        verbose_name = 'category' # 관리자 페이지에서 보여지는 객체가 단수일 때
        verbose_name_plural = 'categories' # 관리자 페이지에서 보여지는 객체가 복수일 때

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_in_category', args=[self.slug])

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True, allow_unicode=True) # allow_unicode: 다양한 언어 지원

    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    meta_description = models.TextField(blank=True) # SEO(Search Engine Optimization) 목적. 검색에 이용.

    price = models.DecimalField(max_digits=10, decimal_places=2) # Decimal : 숫자형으로 바꿔줌.
    stock = models.PositiveIntegerField() # 양수만..?

    available_display = models.BooleanField('Display', default=True) # 상품 노출 여부. 재고 없어도 홍보는 가능하니까.
    available_order = models.BooleanField('Order', default=True) # 상품 주문 가능 여부

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']
        index_together = [['id', 'slug']] # Multi_column index 기능. 두 field 묶어서 index 가능.

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])