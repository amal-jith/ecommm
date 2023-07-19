from django import forms

class CheckoutForm(forms.Form):
    billing_name = forms.CharField(max_length=100)
    billing_email = forms.EmailField()
    billing_address = forms.CharField(max_length=200)
    billing_phone = forms.CharField(max_length=20)
    use_same_shipping_address = forms.BooleanField(required=False)
    shipping_name = forms.CharField(max_length=100, required=False)
    shipping_email = forms.EmailField(required=False)
    shipping_address = forms.CharField(max_length=200, required=False)
    shipping_phone = forms.CharField(max_length=20, required=False)
    card_number = forms.CharField(max_length=16)
    card_expiry = forms.CharField(max_length=5)
    card_cvv = forms.CharField(max_length=3)
