from .models import User,Account,Transaction
from rest_framework import serializers


# 1. Basic serializer 
# Basic Serializer is used to handle input and other external api data without direct database connection
# It has no model dependency,no automated or predinfine so all fields must be defined manually
# here must can add the create update logic as per my wants with the custom logic no predine rule or library like the model serializers 
# Here can add custom logic custom structure, field level and object level valiation so when need more control can use the basic serializer
# It is mainly used for custom logic there no need to store info in the database just only checkig like login,authentication and non model or external api validation

class BasicUserSerializer(serializers.Serializer):
    id=serializers.UUIDField(read_only=True)
    name=serializers.CharField(required=True,max_length=50)
    email=serializers.EmailField(required=True)
    phone=serializers.CharField(max_length=14,required=True)
    nid=serializers.CharField(max_length=15,required=True)
    created_at=serializers.DateTimeField(read_only=True)
    
        # field level validator 
    def validate_email(self,value): 
        
        if self.instance:   # check is it update action 
            a=User.objects.exclude(pk=self.instance.pk)   #if update exclude this pk and search others 
        else:
            a=User.objects.all()   # if new search all user email for check
            
        if a.filter(email=value).exists():
            raise serializers.ValidationError("The email already have")
        return value
    
    def validate_phone(self,value): #field level validator 
        if len(value)>15:
            raise serializers.ValidationError("the phobe number must be in 14 not more")
        return value
    
    
    def validate(self,attrs):   # object level validator 
        if attrs["phone"]==attrs["nid"]:
            raise serializers.ValidationError("the phone and the nid number cant be the sane")
        return attrs
    
    def create(self,validated_data):
        return User.objects.create(**validated_data)
    
    def update(self,instance,validated_data):
        instance.name=validated_data.get("name",instance.name)
        instance.email=validated_data.get("email",instance.email)
        instance.phone=validated_data.get("phone",instance.phone)
        instance.nid=validated_data.get("nid",instance.nid)
        instance.save()
        return instance
    
    
    
    
    
    
    
    
    