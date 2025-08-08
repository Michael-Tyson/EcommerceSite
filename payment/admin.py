from django.contrib import admin
from .models import ShippingAddress,Order,Orderitems
# Register your models here.
admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(Orderitems)
class OrderitemModel(admin.StackedInline):
  model=Orderitems 
  extra=0
class Admin(admin.ModelAdmin):
  model=Order
  readonly_fields=["date"]
  inlines=[OrderitemModel]
admin.site.unregister(Order)
admin.site.register(Order,Admin)