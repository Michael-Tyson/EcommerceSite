from django.urls import path
from . import views
urlpatterns=[
  path("checkout/",views.check_out,name="check_out"),
  path("billinginfo/",views.billing_info,name="billing_info"),
  path("generateorder/",views.generate_order,name="generate_order"),
  path("shippedorder/",views.shipped_orders,name="shipped_orders"),
  path("unshippedorders/",views.unshipped_orders,name="unshipped_orders"),
  path("vieworder/<int:orderid>",views.view_order,name="view_order")
  


]
