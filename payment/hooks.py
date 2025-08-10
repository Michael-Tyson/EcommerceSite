from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from django.dispatch import receiver
from payment.models import Order
import time
@receiver(valid_ipn_received)
def showdata(sender,**kwargs):
  time.sleep(10)
  
  object_obj=sender
  invoice=object_obj.invoice
  order=Order.objects.get(invoice=invoice)
  order.paid=True
  order.save()

  