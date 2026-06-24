from datetime import timezone
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager



class UserManager(BaseUserManager):
    def create_user(self,email,password=None,**extra_fields):
        if not email:
            raise ValueError("the email is required for register")
        email=self.normalize_email(email)# make the email normalize by doint it lower case 
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





class UserSession(models.Model):
    session_id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='session')
    access_token_jti=models.CharField(max_length=350,db_index=True) #token identifier 
    refresh_token_jti=models.CharField(max_length=250,db_index=True)
    device_name=models.CharField(max_length=255,default="unknown_device")
    browser_name=models.CharField(max_length=255,default='Uknown_browser')
    ip_address=models.GenericIPAddressField(null=True,blank=True)
    user_agent=models.TextField(blank=True)
    login_time=models.DateTimeField(auto_now_add=True)
    last_activity=models.DateTimeField(auto_now=True)  #last hit on the api
    expires_at=models.DateTimeField() #expire time
    is_active=models.BooleanField(default=True)
    is_blacklisted=models.BooleanField(default=False)
    
    class Meta:
        db_table="user_session"
        ordering=["-login_time"]
        indexes=[
            models.Index(fields=["user", "is_active"]),
        ]
    
    def __str__(self):
        return f"{self.user.email} ---- {self.device_name} --- {self.login_time}"
    
    def revoke(self): #for revoke it make is active false and mark blacklist true 
        self.is_active=False
        self.is_blacklisted=True
        self.save(update_fields=["is_active","is_blacklisted"]) #then save this fields 
    
    def is_expired(self):
        return timezone.now()>self.expires_at  #check with the timezone now to check and compare session is expired or not 