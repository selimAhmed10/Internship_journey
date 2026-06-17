from rest_framework import serializers

class MoneyField(serializers.Field):
    exchange_rate=120
    
    def to_representation(self, value):
        bdt_balance=float(value)*self.exchange_rate
        return f"{bdt_balance:.2} Taka " 
    
    
    def to_internal_value(self, data):
        try:
            usd_balance=float(data)

        except(TypeError,ValueError):
            raise serializers.ValidationError("The amount must be in numeric.")
    
        if usd_balance<=0:
            raise serializers.ValidationError("the amount must greater than zero or equal")
        return usd_balance