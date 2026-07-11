import uuid
from django.db import models
from django.utils import timezone
from accounts.models import User
import time
import random

class Transaction(models.Model):
    TRANSACTION_TYPES=[
        ('send_money','Send Money'),
        ('cash_in','Cash In'),
        ('cash_out','Cash Out'),
    ]  
    STATUS_CHOICES=[
        ('pending','Pending'),
        ('successful','Successful'),
        ('failed','Failed'),
    ]
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    transaction_id=models.CharField(max_length=50,unique=True,db_index=True)
    transaction_type=models.CharField(max_length=20,choices=TRANSACTION_TYPES)
    status=models.CharField(max_length=20,choices=STATUS_CHOICES, default='pending')
    amount=models.DecimalField(max_digits=15,decimal_places=2)
    
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='sent_trans')
    to_user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='received_transactions',null=True,blank=True)
    agent=models.ForeignKey(User,on_delete=models.CASCADE,related_name='agent_transactions',null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
    class Meta:
        db_table='transactions'
        indexes=[
            models.Index(fields=['transaction_id']),
            models.Index(fields=['user','timestamp']),
        ]
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.transaction_id}-{self.transaction_type} -{self.amount}"
    
    def save(self,*args,**kwargs):
        if not self.transaction_id:
            timestamp=int(time.time())
            random_num=random.randint(10000,99999)
            self.transaction_id=f"TX-{timestamp}-{random_num}"
        super().save(*args,**kwargs)