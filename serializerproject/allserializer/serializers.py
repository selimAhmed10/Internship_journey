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
    
    
    

#Model Serializer 
# ModelSerializer is closely connected with Django models and automatically maps model fields no need to define 
#it is connect to the django model and do the operation using it to read,write and all crud operation and store them in the database
# It reduces boilerplate code by creating the fiel from the model 
# It can automatically handle all crud operation no need to write manually
# It supports meta class where can define model,fields,read_only_fields,write and extra_kwargs
# it is mainly use for the crud operation because of its feature 
    
class AccountModelSerializer(serializers.ModelSerializer):
    class Meta:
        model=Account
        fields= '__all__'
        read_only_fields=[
            'id','created_at'   # only can read this field 
        ]
        
        extra_kwargs={           # can update or create data without this field if in the model it is mendatory field
            "balance":{"required":False},       
            "is_active":{"required":False,"default":True},
            
        }

        
    def validate_balance(self,value):
        if value<0:
            raise serializers.ValidationError("the balance cant negative")
        return value
    
    
    def validate_account_number(self,value):
        if len(value)<10:
            raise serializers.ValidationError("account number must be more than 10 digit")
        return value 
    

     #object level validation for checking is it student account and if it cant store more than 10000 
    def  validate(self,attrs):
        account_type=attrs.get("account_type",self.instance.account_type if self.instance else None)
        balance=attrs.get("balance",self.instance.balance if self.instance else None)
        
        if account_type=="Student" and balance >10000:
            raise serializers.ValidationError("the student account cant store more than 10000")
        return attrs
    


#ListSerializer -- 
#use it for creating the bulk amount of data at a time 
#its automatically run on the backgroun when write serializer.data , many=True 
#Its works on the model seriaizer -- it can works easily but for create the bulk amount the data need logic 
#its mainly work for need to see list of data and create bulk amount of data at a time 
    
class transactionListSerializer(serializers.ListSerializer):
    def validate(self,data):
        if not data:
            raise serializers.ValidationError("The list cant be empty")
        total=sum(item.get("amount",0) for item in data)
        if total>100000:
            raise serializers.ValidationError("total amount mainly exceed the limit for creating data at a time")
        return data


    def create(self,validated_data):
        transaction=[Transaction(**item) for item in validated_data]    
        return Transaction.objects.bulk_create(transaction)
    


#Hyperlink Serializer 
# Hyperlink model serializer use url instead of the primary key for object representation 
# Its generates a url for each user object
# view  name must be match the urls pattern in the urls.py 
# lookup_field="uuid" tells the url use uuid (not the normal id)
# Useful for rest apis that follow HATEOAS principles-hypermedia as the engine of apppilication state , in the link store not only the data also store the additonal informatio



class UserHyperlinkSerializer(serializers.HyperlinkedModelSerializer):
    url=serializers.HyperlinkedIdentityField(view_name="user-detail",lookup_field="uuid")
   
    class Meta:
        model=User
        fields=["url","uuid","name","email","phone","nid","created_at"]
        read_only_fields=["uuid","created_at"]
    



#Read the trasaction info  -- it is mainly use for the report , logs and other here all field marked as read ony
#so the user can only see this cant modify this 
class TrasactionReadOnlySerializer(serializers.ModelSerializer):
    id=serializers.UUIDField(read_only=True)
    account=serializers.PrimaryKeyRelatedField(read_only=True)
    amount=serializers.DecimalField(max_digits=12,decimal_places=2,read_only=True)
    transaction_type=serializers.CharField(read_only=True)
    transaction_status=serializers.CharField(read_only=True)
    note=serializers.CharField(read_only=True)
    created_at=serializers.DateTimeField(read_only=True)
    
    class Meta:
        model=Transaction
        fields=["id","account",'amount','transaction_type','transaction_status','note','created_at']
    
    

    
 



      