from django.db import models
import uuid  #make the unique id number that nobody earlier create 

class Account(models.Model):
    account_type=[
        ('saving','Saving'),
        ('current','Current'),
        ('student','Student')
       
    ]
    
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    account_number=models.CharField(max_length=20,unique=True)
    account_owner=models.CharField(max_length=30)
    account_type=models.CharField(choices=account_type,max_length=50)
    balance=models.DecimalField(max_digits=15,decimal_places=2,default=0)
    is_frozen=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    create_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.account_number}"
