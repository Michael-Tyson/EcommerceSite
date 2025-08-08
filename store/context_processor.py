from .models import Category,Product
import json
from store.models import UserProfile
from django.contrib.auth.models import User
def all_categories(request):
  categories=Category.objects.all()
  return {'categories':categories}
def total_cart(request):
  cart=request.session.get('cart',{})
  
  qty=0
  for value in cart.values():
    qty+=value['qty']
  return {'cart_length':qty}
def totals(request):
  total_price=0
  cart=request.session.get('cart',{})
  sub_totals=dict()

  for key in cart.keys():
    product=Product.objects.get(id=key)
    if product.on_sale:
        sub_totals[key]=product.sale_price*cart[key]['qty']

        total_product_price=product.sale_price*cart[key]['qty']

    else:
      total_product_price=product.price*cart[key]['qty']
    total_price+=total_product_price
  return {'total_price':total_price,'sub_total':sub_totals}


