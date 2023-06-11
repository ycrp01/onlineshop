from decimal import Decimal
from django.conf import settings
from shop.models import Product
from coupon.models import Coupon

# session으로 이용하는 방식. request.session에 data를 저장하고 꺼내오는 방식.
# session에 값 저장하려면 key 설정 필요. settings.py에 CART_ID 만들고 거기에 설정된 값을 가져다가 key로 사용.
class Cart(object):
    # 초기화. Django view에서 사용한 request로 그 안에 session 정보가 들어있음
    def __init__(self, request):
        self.session = request.session # request의 session 정보 가져옴.
        cart = self.session.get(settings.CART_ID) # CART_ID를 cart 변수에 저장. settings에 CART_ID를 만들어야 함.

        if not cart: # CART_ID가 없을 때.
            # cart 정보가 없을 때는 새로운 dictionary 만들어 줌
            cart = self.session[settings.CART_ID] = {}

        self.cart = cart
        self.coupon_id = self.session.get('coupon_id') # session에 저장된 coupon_id 값으로 장바구니에서 할인 금액과 전체 금액 계산.

    def __len__(self): # 장바구니에 들어있는 제품의 quantity 항목들을 전부 더한 결과 제공. 장바구니에 담은 항목의 전체 개수.
        return sum(item['quantity'] for item in self.cart.values())

    def __iter__(self): # for 문 등 사용할 때 어떤 요소들을 건네줄 것인지 지정
        product_ids = self.cart.keys() # 제품들 번호 목록을 가져옴

        # 장바구니에 들어있는 제품들 정보만 Product database에서 가져옴
        products = Product.objects.filter(id__in=product_ids)

        # 제품들 정보 하나씩 읽어옴
        for product in products:
            # session에 키 값들을 넣을 때는 문자로 넣어줌.
            self.cart[str(product.id)]['product'] = product

        # 장바구니에 들어있는 제품들을 하나씩 꺼내는 것
        for item in self.cart.values():
            # 제품 가격, Decimal : 숫자형으로 바꿔서 item에 넣어줌
            item['total_price'] = item['price'] * item['quantity'] # price x item 수
            item['price'] = Decimal(item['price'])

            # Python generator 역할을 함, python 문법 (함수의 return과 유사하나 동작 방식이 조금 다름)
            yield item

    # 제품 장바구니에 넣기
    # is_update : 제품 정보를 업데이트하는지 아닌지 확인하는 것
    def add(self, product, quantity=1, is_update=False):
        product_id = str(product.id) # product_id를 문자로 넣어줌.
        if product_id not in self.cart: # 장바구니에 제품이 없으면
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)} # 해당 제품의 가격을 문자로 넣고, 수량은 0으로 입력.

        if is_update:
            self.cart[product_id]['quantity'] = quantity # 업데이트 된 경우, 변경된 수량으로 덮어쓰기.
        else:
            self.cart[product_id]['quantity'] += quantity # 업데이트 된 게 아니면, 수량 추가.

        self.save()

    # 장바구니에 상품 추가.
    def save(self):
        self.session[settings.CART_ID] = self.cart
        self.session.modified = True

    # 장바구니에서 상품 삭제.
    def remove(self, product):
        product_id = str(product.id) # product_id를 문자로 넣어줌.
        if product_id in self.cart: # 만약 product_id가 cart에 있으면
            del(self.cart[product_id]) # cart에서 해당 product_id 삭제하고
            self.save() # 상태 저장.

    # 장바구니 비우기 기능. 주문 완료 시에도 동작.
    def clear(self):
        self.session[settings.CART_ID] = {}
        self.session['coupon_id'] # 장바구니 비울 때 쿠폰 정보도 함께 삭제해야 함.
        self.session.modified = True

    # 장바구니에 담긴 총 가격 계산.
    def get_product_total(self):
        return sum(Decimal(item['price'])*item['quantity'] for item in self.cart.values())

    @property # coupon을 property 형태로 만들기 위한 decorator. coupon은 method지만, self.coupon과 같이 접근 가능. coupon 키워드로 DB에서 쿠폰 객체 읽어올 수 있음.
    def coupon(self):
        if self.coupon_id:
            return Coupon.objects.get(id=self.coupon_id)

        return None

    def get_discount_total(self): # 할인 금액
        if self.coupon:
            if self.get_product_total() >= self.coupon.amount:
                return self.coupon.amount

        return Decimal(0)

    def get_total_price(self): # 할인 이후 총 금액
        return self.get_product_total() - self.get_discount_total()