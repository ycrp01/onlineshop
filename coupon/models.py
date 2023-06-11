from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True) # 쿠폰 사용시 입력 코드
    use_from = models.DateTimeField() # 쿠폰 사용 기간
    use_to = models.DateTimeField() # 쿠폰 사용 기간
    amount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100000)]) # 할인 금액
    active = models.BooleanField() # 사용 가능 여부

    def __str__(self):
        return self.code
