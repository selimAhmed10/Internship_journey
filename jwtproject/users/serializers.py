from .models import User
from rest_framework import serializers



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


