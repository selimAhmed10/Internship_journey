from .models import User,UserSession
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404


class UserRegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True, required=True)

    class Meta:
        model=User
        fields=['id','email','phone','address','role','password']
        read_only_fields =['id']
        
    def validate_email(self,value):
        if User.objects.filter(email__iexact=value).exists():  # use the iexact for check case sensitive case because email unique if abc@ and ABC@ same for checking use the iexact 
            raise serializers.ValidationError("The email already exists")
        return value.lower()
    
    def create(self,validated_data):
        return User.objects.create_user(**validated_data)


class UserLoginSerializer(serializers.Serializer):
    email=serializers.EmailField()
    password=serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        email=attrs.get('email')
        password=attrs.get('password')
        user=get_object_or_404(User,email__iexact=email)
        user=authenticate(email=email,password=password)
        if not user:
            raise serializers.ValidationError("Invalid password")
        
        refresh=RefreshToken.for_user(user)
        access_token=refresh.access_token
        return {
            'user':user,
            'email':user.email,
            'role':user.role,
            'access':str(access_token),
            'refresh':str(refresh),
            'access_jti':access_token.payload.get('jti'),
            'refresh_jti':refresh.payload.get('jti'),
        }
        
        
class SessionSerializer(serializers.ModelSerializer):
    user_email=serializers.EmailField(source='user.email',read_only=True)
    user_role=serializers.CharField(source='user.role',read_only=True)
    class Meta:
        model=UserSession
        fields='__all__'
        read_only_fields=['session_id','login_time','last_activity','expires_at','is_active','is_blacklisted']






        
        
        