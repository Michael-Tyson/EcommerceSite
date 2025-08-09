from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from store.models import Product,UserProfile
from payment.models import Order,Orderitems
from .models import ShippingAddress
from .forms import ShippingAddressForm,BillingForm
from django.contrib.auth.models import User
from store.context_processor import totals
#paypal stuff
from django.urls import reverse
from django.conf import settings
from paypal.standard.forms import PayPalPaymentsForm
import uuid


# Create your views here.
def success(request):
  return render(request,'payment/success.html')
def failure(request):
  return render(request,'payment/failure.html')
def check_out(request):
  
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
  if request.user.is_authenticated:
    user=User.objects.get(id=request.user.id)
    shipping=ShippingAddress.objects.get(user=user)
    form=ShippingAddressForm(instance=shipping)
  else:
    form=ShippingAddressForm()
    
  context={'products':productslist,'form':form}
  return render(request,"payment/check_out.html",context)
def billing_info(request):
  if request.POST:
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

  
    request.session["shipping_info"]=request.POST
    host=request.get_host()
    paypal_dict={
      'business':settings.PAYPAL_RECEIVER_EMAIL,
      'amount':totals(request)['total_price'],
      'item_name':[product.name for product in products],
      'no_shipping':'2',
      'invoice':str(uuid.uuid4()),
      'currency_code':'USD',
      'notify_url':'https://{}{}'.format(host,reverse("paypal-ipn")),
      'return_url':'https://{}{}'.format(host,reverse("payment_success")),
      'cancel_url':'https://{}{}'.format(host,reverse("payment_failure")),

    }
    paypal_form=PayPalPaymentsForm(initial=paypal_dict)
    billingform=BillingForm()
    return render(request,"payment/billing_info.html",{"shipping_info":request.POST,"billing_form":billingform,'products':productslist,'paypal_form':paypal_form})
  else:
    messages.success(request,"access denied")
    return redirect("home")
def generate_order(request):
  if request.POST:
   
  
    shippingdata=request.session["shipping_info"]
    phone=shippingdata["shipping_phone"]
    fullname=shippingdata["shipping_full_name"]
    address1=shippingdata["shipping_address1"]
    address2=shippingdata["shipping_address1"]
    city=shippingdata["shipping_city"]
    zipcode=shippingdata["shipping_zipcode"]
    state=shippingdata["shipping_state"]
    country=shippingdata["shipping_country"]

    address=f"{address1}\n{address2}\n{city}\n{zipcode}\n{state}\n{zipcode}\n{country}"
    amount=totals(request)
    amount=amount["total_price"]
    if request.user.is_authenticated:
      user=User.objects.get(id=request.user.id)
      order=Order(user=user,phone=phone,shipping_full_name=fullname,address=address,amount=amount)
      order.save()
      cart=request.session.get("cart",{})

      for key,value in cart.items():
         product=Product.objects.get(id=key)
         user=User.objects.get(id=request.user.id)
         price=product.price if not product.on_sale else product.sale_price
         user=User.objects.get(id=request.user.id)
         quantity=value["qty"]
         orderitem=Orderitems.objects.create(order=order,user=user,product=product,price=price,quantity=quantity)
         orderitem.save()
         print("hello")
      
      del request.session['cart']
      userprofile=UserProfile.objects.get(user=user)
         
      userprofile.cart=""
      userprofile.save()

      messages.success(request,"order placed successfully")
      return redirect("home")
    else:
       order=Order(phone=phone,shipping_full_name=fullname,address=address,amount=amount)
       order.save()
       cart=request.session.get("cart",{})

       for key,value in cart.items():
         product=Product.objects.get(id=key)
         
         price=product.price
         quantity=value["qty"]
         orderitem=Orderitems.objects.create(order=order,product=product,price=price,quantity=quantity)
         orderitem.save()
       del request.session["cart"]
    

       messages.success(request,"order placed successfully")
       return redirect("home")


  else:
    messages.success(request,"Access denied")
    return redirect("home")
def shipped_orders(request):
  if request.user.is_authenticated and request.user.is_superuser:
    if request.method=="POST":
      messages.success(request,"shipping status updated")
      id=request.POST["id"]
      order=Order.objects.get(id=id)
      order.shipped=False
      order.save()
      messages.success(request,"shipping status updated")

      return redirect("shipped_orders")

    shipped=Order.objects.filter(shipped=True)
    return render(request,"payment/shipped.html",{"orders":shipped})
  else:
    messages.success(request,"Access Denied")
    return redirect("home")
def unshipped_orders(request):
  if request.user.is_authenticated and request.user.is_superuser:
    if request.method=="POST":
      id=request.POST["id"]
      order=Order.objects.get(id=id)
      order.shipped=True
      order.save()
      
      
      messages.success(request,"shipping status updated")

      return redirect("unshipped_orders")

    unshipped=Order.objects.filter(shipped=False)
    return render(request,"payment/unshipped.html",{"orders":unshipped})
  else:
    messages.success(request,"Access Denied")
    return redirect("home")
def view_order(request,orderid):
  if request.user.is_authenticated and request.user.is_superuser:

    order=Order.objects.get(id=orderid)
    orderitems=Orderitems.objects.filter(order=order)
    context={'order':order,'orderitems':orderitems}
    if request.method=="POST":
      value=request.POST["shipping"]
      if value=="false":
        order.shipped=False
        order.save()
        messages.success(request,"shipping status updated")

        
        return redirect("shipped_orders")
      else:
        order.shipped=True
        order.save()
        messages.success(request,"shipping status updated")

        return redirect("unshipped_orders")

        

    return render(request,'payment/view_order.html',context)