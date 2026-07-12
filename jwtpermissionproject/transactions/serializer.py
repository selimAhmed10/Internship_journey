from rest_framework import serializers
from .models import Transaction,User
import re

class TrasactionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Transaction
        fields='__all__'
        read_only_fields=['id','transaction_id','status','timestamp']

def validate_and_get_user(phone,role=None,exclude_user=None):
    if not phone:
        raise serializers.ValidationError("phone number is required")
    phone=phone.strip()
    if phone.startswith('+8801'):
        phone=phone[3:]
    elif phone.startswith('8801'):
        phone=phone[2:]
    if not re.match(r'^01[3-9]\d{8}$',phone):
        raise serializers.ValidationError("the phone number must startwith 01 and must 11")
    
    try:
        user=User.objects.get(phone_number_wallet_number=phone, is_active=True)
    except User.DoesNotExist:
        raise serializers.ValidationError("No user found using the number ")
    
    if role and user.role!=role:
        raise serializers.ValidationError(f"User is not a {role}")
    
    if exclude_user and user==exclude_user:
        raise serializers.ValidationError("you cant do operation in your own number")
    
    return user


class CashInSerializer(serializers.ModelSerializer):
    customer_phone=serializers.CharField(required=True)
    amount=serializers.DecimalField(required=True,max_digits=15,decimal_places=2,min_value=10)
    class Meta:
        model=Transaction
        fields=['customer_phone','amount']
    
    
    def validate_customer_phone(self,value):
        agent=self.context['request'].user
        user=validate_and_get_user(value,exclude_user=agent,role='customer')
        return user.phone_number_wallet_number
    
    def validate(self,attrs):
        agent=self.context['request'].user
        if agent.balance<attrs['amount']:
            raise serializers.ValidationError(f"insufficient balance ,now amount {agent.balance}")
        return attrs
    
class CashOutSerializer(serializers.ModelSerializer):
    agent_phone=serializers.CharField(required=True)
    amount=serializers.DecimalField(required=True,max_digits=15,decimal_places=2,min_value=10)
    class Meta:
        model=Transaction
        fields=['agent_phone','amount']
    
    
    def validate_agent_phone(self,value):
        customer=self.context['request'].user
        user=validate_and_get_user(value,exclude_user=customer,role='agent')
        return user.phone_number_wallet_number
    
    def validate(self,attrs):
        customer=self.context['request'].user
        if customer.balance<attrs['amount']:
            raise serializers.ValidationError(f"insufficient balance ,now amount {agent.balance}")
        return attrs
    
class SendMoneySerializer(serializers.ModelSerializer):
    recipient_phone=serializers.CharField(required=True)
    amount=serializers.DecimalField(required=True,max_digits=15,decimal_places=2,min_value=10)
    
    class Meta:
        model=Transaction
        fields=['recipient_phone','amount']
    def validate_recipient_phone(self,value):
        sender=self.context['request'].user
        user=validate_and_get_user(value,exclude_user=sender,role='customer')
        return user.phone_number_wallet_number
    
    def validate(self,attrs):
        sender=self.context['request'].user
        if sender.balance<attrs['amount']:
            raise serializers.ValidationError(f"insufficient balance ,now amount {sender.balance}")
        return attrs