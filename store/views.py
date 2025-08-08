from django.shortcuts import render,redirect,get_list_or_404
from .models import Product,Category,UserProfile
import json

from django.http import Http404,HttpResponse
from django.contrib import messages

from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.admin import User
from .forms import SignupForm,UserupdateForm,UpdatepasswordForm,UpdateprofileForm
from payment.forms import ShippingAddressForm
from payment.models import ShippingAddress
def home(request):
	products=Product.objects.all()
	if request.method=="POST":

		query=request.POST["q"].replace(" ","")
	
		if query is not None:
			product1=Product.objects.filter(name__icontains=query)
			product2=Product.objects.filter(description__icontains=query)
			product3=Product.objects.filter(category__name__icontains=query)
			products=product1.union(product2).union(product3)

		
			
	return render(request,'store/index.html',{'products':products})
def about(request):
	return render(request,'store/about.html')
def login_function(request):
	if request.method=="POST":
		name=request.POST["username"]
		password=request.POST["password"]
		user=authenticate(request,username=name,password=password)
		if user is not None:
			login(request,user)
			currentuser=User.objects.get(id=request.user.id)
			userprofile=UserProfile.objects.get(user=currentuser)
			if len(userprofile.cart) != 0:
				cart_saved = json.loads(userprofile.cart)
				request.session["cart"]=cart_saved

			messages.success(request,"logged in successfully")
			return redirect('home')
		else:
			messages.success(request,"username/password incorrect")
			return redirect('login')
	else:
		return render(request,'store/login.html')


	
def logout_function(request):
	logout(request)
	messages.success(request,"Logged out !")
	return redirect('home')
def register(request):
	form=SignupForm()

	if request.method=="POST":
		form=SignupForm(request.POST)
		
		if form.is_valid():
			form.save()
			username=request.POST["username"]
			password=request.POST["password1"]
		
			user=authenticate(request,username=username,password=password)
			if user is not None:
				login(request,user)
			messages.success(request,"Thanks for registering")

			return redirect('home')
		else:
			print(list(form.errors.values()))
			for error in list(form.errors.values()):

				messages.error(request,error)
			return redirect('register')
	else:
		return render(request,'store/register.html',{"form":form})
		
def product(request,product_id):
	product=Product.objects.get(id=product_id)
	

	context={'product':product}
	return render(request,'store/product.html',context)
def category(request,cat_name):
	categories=Category.objects.all()
	try:
		category=Category.objects.get(name=cat_name)
	except Category.DoesNotExist:
		
		return render(request,'store/notfound.html')
	

	
	products=Product.objects.filter(category=category)
	return render(request,'store/category.html',{'products':products,'category':category})
def all_categories(request):
	categories=Category.objects.all()
	return render(request,'store/categories.html',{'categories':categories})
def update_user(request):
	if request.user.is_authenticated:
		user=User.objects.get(id=request.user.id)
		form=UserupdateForm(instance=user)
		if request.method=="POST":
			form=UserupdateForm(request.POST,instance=user)
			if  form.is_valid():
				form.save()
				messages.success(request,"user updated successfully")
				return redirect('home')
			else:
				messages.success(request,"There was some error")
				return redirect('update_user')
		else:
			return render(request,'store/user_change.html',{'form':form})
	else:
		messages.success(request,"You need to log in to access this page")
		return redirect('login')
def update_password(request):
	if request.user.is_authenticated:
		user=User.objects.get(id=request.user.id)
		form=UpdatepasswordForm(instance=user)
		if request.method=="POST":
					
					form=UpdatepasswordForm(user,request.POST)
					if form.is_valid():
						form.save()
						
						messages.success(request,"password updation successfull\nLogin again")
						return redirect("login")
					else:
						for error in list(form.errors.values()):
							print(error)
							print("there is some error")
							messages.error(request,error)
						return redirect("update_password")
		else:
			return render(request,"store/update_password.html",{"form":form})
	else:
		messages.success(request,"you need to login first")
		return redirect("login")


def update_profile(request):
	

	if request.user.is_authenticated:
		user=User.objects.get(id=request.user.id)
		userprof=UserProfile.objects.get(user=user)
		form=UpdateprofileForm(instance=userprof)

		shippingaddress=ShippingAddress.objects.get(user=user)

	
		shipping_form=ShippingAddressForm(instance=shippingaddress)
		if request.method=="POST":
			form=UpdateprofileForm(request.POST,instance=userprof)
			shipping_form=ShippingAddressForm(request.POST,instance=shippingaddress)
	
			if form.is_valid() or shipping_form.is_valid():
		
				form.save()
				
				shipping_form.save()
				messages.success(request,"user updated successfully")
				return redirect("home")
			else:
				messages.success(request,"There was some error")
				return redirect('update_profie')
		else:
			return render(request,'store/profile_update.html',{'form':form,'shipping_form':shipping_form})
	else:
		messages.success(request,"You need to log in to access this page")
		return redirect('login')


