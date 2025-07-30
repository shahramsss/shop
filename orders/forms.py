from django import forms


class CartAddForm(forms.Form):
    quantity = forms.IntegerField(label="تعداد",min_value=1)

    
class CouponApplayForm(forms.Form):
    code = forms.CharField(label="کد تخفیف" , widget=forms.TextInput(attrs={"class": "form-control",}))