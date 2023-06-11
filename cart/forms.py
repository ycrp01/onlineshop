# 카트 기능을 사이트에서 사용하기 위해 뷰 생성
# 카트 기능은 사용자에게 입력 받기 때문에 폼을 만들어 뷰에서 활용하는 방식으로 기능 구현

from django import forms

class AddProductForm(forms.Form):
    quantity = forms.IntegerField() # 제품 수량.
    is_update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput) # 페이지마다 update 방식 다르게 하기 위한 변수.