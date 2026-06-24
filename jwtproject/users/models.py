import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager



class UserManager(BaseUserManager):
    def create_user(self,email,password=None,**extra_fields):
        if not email:
            raise ValueError("the email is required for register")
        email=self.normalize_email(email)   # make the email normalize by doint it lower case 
        if 'username' not in extra_fields or not extra_fields['username']:extra_fields['username']=email   # if the field dont have the username take email as the user name for it 
        user=self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email,password=None,**extra_fields):
        extra_fields.setdefault("is_staff",True)
        extra_fields.setdefault("is_superuser",True)
        extra_fields.setdefault("is_active",True)
        extra_fields.setdefault("role","admin")
        return self.create_user(email,password,**extra_fields)


class User(AbstractUser):
    ROLE_CHOICES=(
        ("admin","Admin"),
        ("customer","Customer"),
        ("agent","Agent"),
        ("merchant","Merchant"),
    )
    
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    email=models.EmailField(max_length=30,unique=True,db_index=True)
    phone=models.CharField(max_length=14,unique=True,db_index=True)
    address=models.CharField(max_length=255,blank=True,null=True)
    role=models.CharField(max_length=20,choices=ROLE_CHOICES,default="customer",db_index=True)
    objects=UserManager()
    USERNAME_FIELD="email"   #set username as email for login using the email field
    REQUIRED_FIELDS=[]   
    
    class Meta:
        db_table="users"
        ordering=["-date_joined"]
        indexes=[models.Index(fields=["email", "is_active"])]
    
    def __str__(self):
        return self.email
    
    def save(self,*args,**kwargs):    # username field set with the email and save it 
        if not self.username:
            self.username = self.email
        super().save(*args, **kwargs)
    
    @property
    def is_admin(self):
        return self.role=="admin"
    
    @property
    def is_customer(self):
        return self.role=="customer"
    
    @property
    def is_agent(self):
        return self.role=="agent"
    
    @property
    def is_merchant(self):
        return self.role=="merchant"
