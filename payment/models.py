from django.db import models
from django.contrib.auth.models import User
from store.models import Product
from django.dispatch import receiver
from django.utils import timezone
from django.db.models.signals import pre_save,post_save
class ShippingAddress(models.Model):
  user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
  shipping_full_name=models.CharField(max_length=100)
  shipping_phone=models.CharField(max_length=20)
  shipping_address1=models.CharField(max_length=100)
  shipping_address2=models.CharField(max_length=100,blank=True,null=True)
  shipping_city=models.CharField(max_length=100)
  shipping_state=models.CharField(max_length=100,blank=True,null=True)
  shipping_zipcode=models.CharField(max_length=100,blank=True,null=True)
  shipping_country=models.CharField(max_length=100)
  class Meta:
    verbose_name_plural="Shipping Addresses"
  def __str__(self):
    return f"shipping_address: {self.id}"  
class Order(models.Model):
  user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
  shipping_full_name=models.CharField(max_length=100)
  phone=models.CharField(max_length=100)
  address=models.TextField()
  amount=models.DecimalField(max_digits=6,decimal_places=2)
  date=models.DateTimeField(auto_now_add=True)
  shipped=models.BooleanField(default=False)
  shipping_date=models.DateTimeField(null=True,blank=True)
  def __str__(self):
    return f"Order-{self.id}"
class Orderitems(models.Model):
  product=models.ForeignKey(Product,on_delete=models.CASCADE,blank=True,null=True)
  user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
  order=models.ForeignKey(Order,on_delete=models.CASCADE,null=True)
  quantity=models.PositiveIntegerField()
  price=models.DecimalField(max_digits=6,decimal_places=2)
  def __str__(self):
    return f"orderitem-{self.id}"



@receiver(post_save,sender=User)
def createprofile(*args,**kwargs):
  

  if kwargs["created"]:
    shipadd=ShippingAddress(user=kwargs["instance"])
    shipadd.save()
def adddate(sender,instance,*args,**kwargs):
  if instance.pk:
    obj=sender._default_manager.get(id=instance.pk)
    if instance.shipped and not obj.shipped:
      instance.shipping_date=timezone.now()
    

      

pre_save.connect(adddate,sender=Order)

  