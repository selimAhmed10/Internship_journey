
import uuid
from django.db import models
from django.db.models import Q,CheckConstraint

class User(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    name=models.CharField(max_length=50)
    email=models.EmailField(unique=True)
    phone=models.CharField(max_length=14,unique=True)
    nid=models.CharField(max_length=15,unique=True)
    created_at=models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering=["-created_at"]
        indexes=[
            models.Index(fields=["created_at"]),
        ]
        
        
    def __str__(self):
        return self.email
    



class Account(models.Model):
    
    account_ty=(
        ('Savings','savings'),
        ('Current','current'),
        ('Student','student'),
    )

    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    account_number=models.CharField(max_length=50,unique=True)
    account_type=models.CharField(choices=account_ty,default='savings',max_length=20)
    balance=models.DecimalField(max_digits=15,decimal_places=2,default=0)
    is_active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering=["-created_at"]
        indexes=[
            models.Index(fields=["account_number"]),
            models.Index(fields=["user"]),
            models.Index(fields=["is_active"]),
        ]

        constraints=[
            CheckConstraint(
                condition=Q(balance__gte=0),
                name="Account_balance_cant_negetive"
            )
        ]
    def __str__(self):
        return self.account_number
    
    
    


class Transaction(models.Model):
    
    trans_type=(
        ('Deposit','deposit'),
        ('Withdraw','withdraw'),
        ('Transfer','transfer'),
        
    )
    trans_sta=(
        ('Pending','pending'),
        ('Successful','successful'),
        ('Failed','failed'),
    )
    
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    account=models.ForeignKey(Account,on_delete=models.CASCADE)
    amount=models.DecimalField(max_digits=12,decimal_places=2,default=0)
    transaction_type=models.CharField(choices=trans_type,default='deposit',max_length=20)
    transaction_status=models.CharField(choices=trans_sta,default='pending',max_length=20)
    note=models.CharField(max_length=100,blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    

    class Meta:
        ordering=["-created_at"]

        indexes=[
            models.Index(fields=["account"]),
            models.Index(fields=["transaction_type"]),
            models.Index(fields=["transaction_status"]),
            models.Index(fields=["created_at"]),
        ]

        constraints = [
            CheckConstraint(
                condition=Q(amount__gte=0),
                name="transaction_amount_must_positive"
            )
        ]

    def __str__(self):
        return (
            f"{self.transaction_type}-{self.amount}"
        )
