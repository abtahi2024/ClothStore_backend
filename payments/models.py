from django.db import models
from users.models import User
from order.models import Order
# Create your models here.
class Payment(models.Model):
    PENDING = 'pending'
    SUCCESS = 'success'
    FAILED = 'failed'
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (SUCCESS, 'Success'),
        (FAILED, 'Failed'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='payments')
    oreder=models.OneToOneField(Order,on_delete=models.CASCADE,related_name='payment')
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default=PENDING)
    transaction_id = models.CharField(max_length=100,blank=True,null=True)

    def __str__(self):
        return f"Payment {self.id} - {self.status}"
