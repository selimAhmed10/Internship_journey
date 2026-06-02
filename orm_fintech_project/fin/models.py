from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Q,UniqueConstraint,CheckConstraint
import uuid
from datetime import date, timedelta

#Custtom manager for for battter quarty performance and code organization

class UserManager(models.Manager):
    def admins(self):
        return self.filter(role='admin')
    
    def customers(self):
        return self.filter(role='customer')
    
    def merchants(self):
        return self.filter(role='merchant')
    
    def agents(self):
        return self.filter(role='agent')


class AccountManager(models.Manager):
    def active_accounts(self):
        return self.filter(status='active')
    
    def by_type(self, account_type):
        return self.filter(account_type=account_type)


class TransactionManager(models.Manager):
    def successful(self):
        return self.filter(status='success')
    
    def failed(self):
        return self.filter(status='failed')


class CardManager(models.Manager):
    def active_cards(self):
        return self.filter(status='active')
    
    def expired_cards(self):
        return self.filter(expiry_date__lt=date.today())


class MerchantManager(models.Manager):
    def active_merchants(self):
        return self.filter(is_active=True)


#User model with role-based design and indexing for phone and role fields for better query performance

class User(AbstractUser):
    Role= [
        ('admin','Admin'),
        ('customer','Customer'),
        ('merchant','Merchant'),
        ('agent','Agent'),
    ]

    name=models.CharField(max_length=100)
    email=models.EmailField(unique=True)
    phone=models.CharField(max_length=20,unique=True,db_index=True)
    role=models.CharField(max_length=20,choices=Role,default='customer',db_index=True)
    created_at=models.DateTimeField(auto_now_add=True)
    objects=UserManager()
    
    class Meta:
        indexes=[
            models.Index(fields=['phone']),
            models.Index(fields=['role']),
        ]

    def __str__(self):
        return f"{self.name} ({self.role})"



#Account model 


class Account(models.Model):
    Accounts_type=[
        ('saving','Saving'),
        ('student','Student'),
        ('fixed','Fixed Deposit'),
    ]

    Status= [
        ('active','Active'),
        ('blocked','Blocked'),
        ('frozen','Frozen'),
    ]

    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='accounts')
    account_number=models.CharField(max_length=30,unique=True,db_index=True)
    account_type=models.CharField(max_length=20,choices=Accounts_type,default='saving',db_index=True)
    status=models.CharField(max_length=20,choices=Status,default='active',db_index=True)
    balance=models.DecimalField(max_digits=12,decimal_places=2,default=0)
    created_at=models.DateTimeField(auto_now_add=True)

    objects = AccountManager()

    class Meta:
        indexes = [
            models.Index(fields=['account_number']),
            models.Index(fields=['status']),
            models.Index(fields=['account_type']),
            models.Index(fields=['user','status']),
        ]
        constraints = [
            models.CheckConstraint(check=Q(balance__gte=0), name='balance_non_negative'),
        ]

    def __str__(self):
        return f"{self.account_number} - {self.status}"



#card model 

class Card(models.Model):
    Card_type=[
        ('debit','Debit'),
        ('credit','Credit'),
    ]

    Status= [
        ('active','Active'),
        ('blocked','Blocked'),
        ('expired','Expired'),
    ]

    # One account can have one card
    account=models.OneToOneField(Account,on_delete=models.CASCADE)
    card_number=models.CharField(max_length=16,unique=True,db_index=True)
    card_type=models.CharField(max_length=10,choices=Card_type)
    status=models.CharField(max_length=20,choices=Status,default='active',db_index=True)
    expiry_date=models.DateField()
    created_at=models.DateTimeField(auto_now_add=True)

    objects = CardManager()

    class Meta:
        indexes = [
            models.Index(fields=['card_number']),
            models.Index(fields=['status']),
            models.Index(fields=['expiry_date']),
        ]

    def __str__(self):
        return self.card_number

    def is_expired(self):
        return self.expiry_date < date.today()


#Marchent model with category and indexing for better query performance
class Merchant(models.Model):
    Category= [
        ('ecommerce','Ecommerce'),
        ('grocery','Grocery'),
        ('utility','Utility'),
        ('other', 'Other'),
    ]

    name=models.CharField(max_length=100,db_index=True)
    merchant_id=models.CharField(max_length=20,unique=True,db_index=True)
    category = models.CharField(max_length=20,choices=Category,db_index=True)
    is_active = models.BooleanField(default=True,db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = MerchantManager()

    class Meta:
        indexes = [
            models.Index(fields=['merchant_id']),
            models.Index(fields=['category']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return self.name


#traanssactions model 
class Transaction(models.Model):
    Tractions_type=[
        ('debit','Debit'),
        ('credit','Credit'),
    ]

    Status= [
        ('success','Success'),
        ('failed','Failed'),
        ('pending','Pending'),
    ]

    account=models.ForeignKey(Account,on_delete=models.CASCADE,related_name='transactions')
    merchant=models.ForeignKey(Merchant,on_delete=models.SET_NULL,null=True,blank=True)
    card=models.ForeignKey(Card,on_delete=models.SET_NULL,null=True,blank=True,)
    amount=models.DecimalField(max_digits=12,decimal_places=3)
    transaction_type=models.CharField(max_length=10, choices=Tractions_type)
    status=models.CharField(max_length=10,choices=Status,default='pending',db_index=True)
    reference_id=models.CharField(max_length=50,unique=True,db_index=True)
    created_at=models.DateTimeField(auto_now_add=True, db_index=True)

    objects = TransactionManager()

    class Meta:
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['created_at']),
            models.Index(fields=['account']),
            models.Index(fields=['reference_id']),
        ]
        constraints = [
            models.CheckConstraint(check=Q(amount__gt=0), name='positive_transaction_amount'),
        ]

    def __str__(self):
        return f"{self.reference_id} - {self.status}"