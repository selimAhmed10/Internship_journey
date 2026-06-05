from django.db import models
from accounts.models import Account
import uuid

class Transaction(models.Model):
    types=[
        ('Credit','credit'),
        ('Debit','debit'),
    ]
    transaction_status=[
        ('Success','success'),
        ('Failed','failed'),
        ('Pending','Pending'),
    ]
    
    trans_id=models.UUIDField(primary_key =True,default=uuid.uuid4,editable=False)
    account=models.ForeignKey(Account,on_delete=models.CASCADE,related_name='transactions')
    amount=models.DecimalField(max_digits=12,decimal_places=2)
    transaction_type=models.CharField(max_length=10,choices=types)
    status=models.CharField(max_length=10,choices=transaction_status,default='pending')
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.trans_id}"
