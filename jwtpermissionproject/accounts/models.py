import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES=[
        ('customer','Customer'),
        ('agent','Agent'),
        ('admin','Admin'),
    ]  
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    phone_number_wallet_number=models.CharField(max_length=14,unique=True,db_index=True,null=True,blank=True)
    email=models.EmailField(unique=True,db_index=True)
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    address=models.TextField()
    role=models.CharField(max_length=20,choices=ROLE_CHOICES,default='customer')
    balance=models.DecimalField(max_digits=15,decimal_places=2,default=0.00)
    is_verified=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table='users'
        indexes=[
            models.Index(fields=['phone_number_wallet_number']),
            models.Index(fields=['role']),
        ]

    def __str__(self):
        return f"{self.username} ({self.role})"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()