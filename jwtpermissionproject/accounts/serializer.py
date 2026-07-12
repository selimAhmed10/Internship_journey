from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
import re
from .models  import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True,required=True,validators=[validate_password])
    class Meta:
        model=User
        fields='__all__'    
    
    def validate_phone_number_wallet_number(self,value):
        if value:
            value=value.strip()
        if value.startswith('+8801'):
            value = value[3:]
        elif value.startswith('8801'):
            value = value[2:]
            
        if not re.match(r'^01[3-9]\d{8}$',value):
            raise serializers.ValidationError("Phone number must be start with 01 and 11 digit")
        return value
    
    def validate(self, attrs):  # for the admin no need wallet number and other field need
        role=attrs.get('role')
        if role=='admin':
            errors={}
            if not attrs.get('email'):
                errors['email']="Email is required for admin"
            if not attrs.get('first_name'):
                errors['first_name']="First name is required for admin"
            if not attrs.get('last_name'):
                errors['last_name']="Last name is required for admin"
            if not attrs.get('address'):
                errors['address']="Address is required for Admin"
            if errors:
                raise serializers.ValidationError(errors)
            
            attrs['phone_number_wallet_number']=None
        
        else:   #for the agent and customer need to fill all the field 
            errors={}
            if not attrs.get('phone_number_wallet_number'):
                errors['phone_number_wallet_number']=f"Phone number is required for {role}"
            if not attrs.get('email'):
                errors['email']=f"Email is required for {role}"
            if not attrs.get('first_name'):
                errors['first_name']=f"First name is required for {role}"
            if not attrs.get('last_name'):
                errors['last_name']=f"Last name is required for {role}"
            if not attrs.get('address'):
                errors['address']=f"Address is required for {role}"
            if errors:
                raise serializers.ValidationError(errors)
        return attrs
    
    def create(self, validated_data):
        user=User.objects.create_user(**validated_data)
        return user

class UserLoginSerializer(serializers.Serializer):
    username=serializers.CharField(required=True)
    password=serializers.CharField(required=True,write_only=True)
    
    def validate(self,attrs):
        username=attrs.get('username')
        password=attrs.get('password')
        
        if username and password:
            user=authenticate(username=username,password=password)
            if not user:
                raise serializers.ValidationError("usee not have ")
            if not user.is_active:
                raise serializers.ValidationError("Account is not activate")
        else:
            raise serializers.ValidationError("use valid username and password") 
        attrs['user']=user
        return attrs
    
class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields ='__all__'
        

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','phone_number_wallet_number','email', 'first_name','last_name','address','role', 'balance', 'is_active', 'is_verified']
    
    def validate_phone_number_wallet_number(self,value):
        if value:
            value=value.strip()
            if value.startswith('+8801'):
                value=value[3:]
            elif value.startswith('8801'):
                value=value[2:]
            
            if not re.match(r'^01[3-9]\d{8}$', value):
                raise serializers.ValidationError("Phone number must start with 01 and be 11 digits")
        return value


class UserCreateSerializer(serializers.ModelSerializer):
    password=serializers.CharField(
        write_only=True, 
        required=True, 
        validators=[validate_password]
    )
    class Meta:
        model=User
        fields=['username','password','phone_number_wallet_number','email', 'first_name', 'last_name', 'address','role','balance','is_active','is_verified']
    
    def validate_phone_number_wallet_number(self, value):
        if value:
            value=value.strip()
            if value.startswith('+8801'):
                value=value[3:]
            elif value.startswith('8801'):
                value=value[2:]
            
            if not re.match(r'^01[3-9]\d{8}$', value):
                raise serializers.ValidationError("Phone number must start with 01 and be 11 digits")
        return value
    
    def create(self, validated_data):
        user=User.objects.create_user(**validated_data)
        return user

