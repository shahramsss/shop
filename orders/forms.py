from django import forms


class CartAddForm(forms.Form):
    quantity = forms.IntegerField(label="تعداد",min_value=1)

    
