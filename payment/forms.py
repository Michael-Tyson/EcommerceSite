from .models import ShippingAddress
from django import forms
class ShippingAddressForm(forms.ModelForm):  
  shipping_full_name=forms.CharField(max_length=100,label="",widget=forms.TextInput(attrs=({'class':'form-control','placeholder':"Enter full name"})))
  shipping_phone=forms.CharField(max_length=20,widget=forms.TextInput(attrs=({'class':'form-control','placeholder':"Enter phone"})))
  shipping_address1=forms.CharField(max_length=100,widget=forms.TextInput(attrs=({'class':'form-control','placeholder':"Enter shipping address"})))
  shipping_address2=forms.CharField(max_length=100,required=False,widget=forms.TextInput(attrs=({'class':'form-control','placeholder':"Enter shipping address"})))
  shipping_city=forms.CharField(max_length=100,widget=forms.TextInput(attrs=({'class':'form-control','placeholder':"Enter city"})))
  shipping_state=forms.CharField(max_length=100,required=False, widget=forms.TextInput(attrs=({'class':'form-control','placeholder':"Enter State"})))
  shipping_zipcode=forms.CharField(max_length=100,required=False, widget=forms.TextInput(attrs=({'class':'form-control','placeholder':"Enter zipcode"})))
  shipping_country=forms.CharField(max_length=100,widget=forms.TextInput(attrs=({'class':'form-control','placeholder':"Enter country"})))
  class Meta:
    model=ShippingAddress
    fields=('shipping_full_name','shipping_phone','shipping_address1','shipping_address2','shipping_city','shipping_state','shipping_zipcode','shipping_country')
    exclude=['user',]
class BillingForm(forms.Form):
    card_name=forms.CharField(max_length=100,label="",widget=forms.TextInput(attrs=({'class':'form-control','placeholder':"Name on card"})))
    card_number= forms.CharField(max_length=100,label="",widget=forms.TextInput(attrs=({'class':'form-control','placeholder':"Card number"})))
    card_expiry=forms.DateField(label="",widget=forms.TextInput(attrs=({'class':'form-control','placeholder':"dd/mm/yyyy"})))
    card_cvv_number=forms.IntegerField(label="",widget=forms.TextInput(attrs=({'class':'form-control','placeholder':"CVV number"})))
    billing_address1=forms.CharField(max_length=100,widget=forms.TextInput(attrs=({'class':'form-control','placeholder':"Enter billing address"})))
    billing_address2=forms.CharField(max_length=100,required=False,widget=forms.TextInput(attrs=({'class':'form-control','placeholder':"Enter billing address"})))
    billing_city=forms.CharField(max_length=100,widget=forms.TextInput(attrs=({'class':'form-control','placeholder':"Enter city"})))
    billing_state=forms.CharField(max_length=100,required=False, widget=forms.TextInput(attrs=({'class':'form-control','placeholder':"Enter State"})))
    billing_zipcode=forms.CharField(max_length=100,required=False, widget=forms.TextInput(attrs=({'class':'form-control','placeholder':"Enter zipcode"})))
    billing_country=forms.CharField(max_length=100,widget=forms.TextInput(attrs=({'class':'form-control','placeholder':"Enter country"})))

