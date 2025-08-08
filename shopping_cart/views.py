
from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from store.models  import Product
import json
from store.models import UserProfile
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@csrf_exempt
def add_cart(request):
  if request.method=="GET":
    return JsonResponse({'message':"only fucking post request accepted"})

  else:
    data=json.loads(request.body)
    product_id=data.get('product_id',"")
    product_qty=int(data.get('product_qty',""))
    product=Product.objects.get(id=product_id)
    cart=request.session.get('cart',{})
    
    if product_id in cart:
          messages.success(request,"Item already present in cart")

    else:
          messages.success(request,"Item added to  cart")
    cart[product_id]={'qty':product_qty}
    
    request.session['cart']=cart
    request.session.modified=True
    
    if request.user.is_authenticated:
      currentuser=User.objects.get(id=request.user.id)
      userprofile=UserProfile.objects.get(user=currentuser)
      userprofile.cart=json.dumps(cart)
      userprofile.save()
    
    quantity=0
    for key in cart:
      quantity+=cart[key]['qty']
    resopnse=JsonResponse({"product_id":product_id,"quantity":quantity})
    return resopnse
  # cart=request.session.get('cart',{})

def view_cart(request):
  cart=request.session.get("cart",{})

  keys=list()
  for key in cart:
    keys.append(key)
  products=Product.objects.filter(id__in=keys)
  index=0
  productslist=[i for i in range(len(products))]
  for product in products:
    product={'product':product,'qty':cart[str(product.id)]['qty'],'sub_total':product.price*cart[str(product.id)]['qty'] if not product.on_sale else product.sale_price*cart[str(product.id)]['qty']}
    productslist[index]=product
    index+=1
  
  context={'products':productslist}
  return render(request,'shopping_cart/view.html',context)
@csrf_exempt
def update_cart(request):
  if request.method!="POST":
    return JsonResponse({"message":"only post requested accepted"})
  else:
    data=json.loads(request.body)
    product_id=data.get('product_id',"")
    product_qty=int(data.get('product_qty',""))
    
    cart=request.session.get('cart',{})
    cart[product_id]["qty"]=product_qty
    request.session["cart"]=cart
    request.session.modified=True
    if request.user.is_authenticated:
      currentuser=User.objects.get(id=request.user.id)
      userprofile=UserProfile.objects.get(user=currentuser)
      userprofile.cart=json.dumps(cart)
      userprofile.save()
    
    quantity=0
    for key in cart:
      quantity+=cart[key]['qty']
    resopnse=JsonResponse({"product_id":product_id,"quantity":quantity})
    messages.success(request,"Cart items updated")
    return resopnse

@csrf_exempt
def delete_cart(request):
  if request.method!="POST":
    return JsonResponse({"message":"only post requested accepted"})
  else:
    data=json.loads(request.body)
    product_id=data.get('product_id',"")
    
    
    cart=request.session.get('cart',{})
    del cart[product_id]

    request.session["cart"]=cart
    request.session.modified=True
    if request.user.is_authenticated:
      currentuser=User.objects.get(id=request.user.id)
      userprofile=UserProfile.objects.get(user=currentuser)
      userprofile.cart=json.dumps(cart)
      userprofile.save()

    quantity=0
    for key in cart:
      quantity+=cart[key]['qty']
    resopnse=JsonResponse({"product_id":product_id,"quantity":quantity})
    messages.success(request,"Item deleted from Cart")
    return resopnse

  