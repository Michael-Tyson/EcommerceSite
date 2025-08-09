from django.db import models
from django.shortcuts import redirect
from django.db.models.signals import (post_save)
from datetime import datetime as dt
from django.contrib.auth.models import User
from django.dispatch import receiver

# Create your models here.
class Category(models.Model):
  name=models.CharField(max_length=100)
  
  class Meta():
    verbose_name='Category'
    verbose_name_plural='Categories'
  def __str__(self):
    return self.name

class Product(models.Model):
  name=models.CharField(max_length=200)
  category=models.ForeignKey(Category,on_delete=models.CASCADE)
  image=models.ImageField(default='product.jpg',null=True)
  price=models.DecimalField(decimal_places=2,max_digits=6,default=0.0)
  description=models.TextField(default="",blank=True,null=True)
  on_sale=models.BooleanField(default=False)
  sale_price=models.DecimalField(decimal_places=2,max_digits=6,default=0.0)
  def __str__(self):
    return self.name

class Customer(models.Model):
  firstname=models.CharField(max_length=100)
  lastname=models.CharField(max_length=100)
  phone=models.CharField(max_length=20)
  email_address=models.EmailField()
  
  def __str__(self):
    return f"{self.firstname} {self.lastname}"
order_status=[
  ("P","pending"),
  ("S","shipped"),
  ("D","delivered"),
]
class Order(models.Model):
  product=models.ForeignKey(Product,on_delete=models.CASCADE)
  customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
  items=models.IntegerField(default=1)
  date=models.DateTimeField(default=dt.today)
  totalprice=models.DecimalField(max_digits=10,decimal_places=2,blank=True)
  status=models.CharField(choices=order_status,max_length=1,default='P')
  def __str__(self):
    return f"ordered {self.product} by {self.customer}"
class UserProfile(models.Model):
  user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")
  date_modified=models.DateTimeField(User,auto_now=True)
  phone=models.CharField(max_length=20,blank=True)
  address1=models.CharField(max_length=100,blank=True)
  address2=models.CharField(max_length=100,blank=True)
  city=models.CharField(max_length=100,blank=True)
  state=models.CharField(max_length=100,blank=True)
  zipcode=models.CharField(max_length=100,blank=True)
  country=models.CharField(max_length=100,blank=True)
  cart=models.CharField(max_length=1000,blank=True,null=True,default="")
  def __str__(self):
    return self.user.username

 

def create(sender,created,instance,**kwargs):
  if created:
    user_profile=UserProfile(user=instance)
    user_profile.save()
post_save.connect(create,sender=User)



  



