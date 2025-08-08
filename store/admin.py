from django.contrib import admin
from django.contrib.auth.models import User
from .models import Customer,Category,Order,Product,UserProfile



# Register your models here.
admin.site.register(Customer)

admin.site.register(Category)
admin.site.register(Order)
admin.site.register(Product)
admin.site.register(UserProfile)
class Profile(admin.StackedInline):
  model=UserProfile
class Admin(admin.ModelAdmin):
  model=User
  fields=["username","first_name","last_name","email"]
  inlines=[Profile]
admin.site.unregister(User)
admin.site.register(User,Admin)