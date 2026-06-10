from rest_framework import serializers
from .models import Account

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'
        
        
class AccountListSerializer(serializers.ModelSerializer):
    class Meta:
        model=Account
        fields =['id','account_number','account_owner','balance']
        #here i can use also the exclude 
        #for adding new field can use - serializerFieldMethod()
        #can have read only or can use kwarg for add more behaviour like required or not 
        #can use torepresentation,writeonly,tointernalvalue and more 
        #can use validation and more can be custom also 


class AccountDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model=Account
        fields ='__all__'
        read_only_fields =['id','create_at']