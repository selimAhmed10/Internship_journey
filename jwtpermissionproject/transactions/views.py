from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.db.models import F, Q
from .models import Transaction,User
from .serializer import TrasactionSerializer,CashInSerializer,CashOutSerializer,SendMoneySerializer
from permissions.custom_permissions import IsAdmin, IsAgent, IsCustomer

class AdminDashboard(APIView):
    permission_classes=[IsAdmin]
    
    def get(self,request):
        user= request.user
        total_customer=User.objects.filter(role='customer').count()
        total_agents=User.objects.filter(role='agent').count()
        total_transaction=Transaction.objects.count()
        return Response({
            'name': user.full_name,
            'role': user.role,
            'email': user.email,
            'total_customers': total_customer,
            'total_agents': total_agents,
            'total_transactions':total_transaction,
        })
        
class AdminAllTransactionsView(APIView):
    permission_classes=[IsAdmin]
    def get(self,request):
        transactions=Transaction.objects.all()[:20]
        serializer=TrasactionSerializer(transactions,many=True)
        return Response(serializer.data)

class AgentDashboard(APIView):
    permission_classes=[IsAgent]
    def get(self,request):
        user = request.user
        return Response({
            'name':user.full_name,
            'role':user.role,
            'phone':user.phone_number_wallet_number,
            'balance':user.balance,
        })
        
class AgentTransaction(APIView):
    permission_classes=[IsAgent]
    def get(self,request):
        transactions=Transaction.objects.filter(Q(agent=request.user)|Q(user=request.user))[:20]
        data=[]        
        for t in transactions:
            data.append({
                'timestamp':t.timestamp.strftime('%Y-%m-%d %H:%M'),
                'transaction_id':t.transaction_id,
                'wallet_number':t.user.phone_number_wallet_number,
                'type':t.get_transaction_type_display(),
                'amount':str(t.amount),
                'status':t.status,
            })
        return Response(data)
    
class CashIn(APIView):
    permission_classes=[IsAgent]
    def post(self,request):
        cashise=CashInSerializer(data=request.data,context={'request':request})
        cashise.is_valid(raise_exception=True)
        customer_phone=cashise.validated_data['customer_phone']
        amount=cashise.validated_data['amount']
        
        try:
            customer=User.objects.get(phone_number_wallet_number=customer_phone)
        except User.DoesNotExist:
            return Response({'error':'the customer not found'},status=status.HTTP_404_NOT_FOUND)
        
        try:
            with transaction.atomic():
                agent=User.objects.select_for_update().get(id=request.user.id)
                customer=User.objects.select_for_update().get(id=customer.id)
                agent.balance=F('balance')-amount
                agent.save(update_fields=['balance'])
                customer.balance=F('balance')+amount
                customer.save(update_fields=['balance'])
                transaction_obj=Transaction.objects.create(
                    user=customer,
                    agent=agent,
                    transaction_type='cash_in',
                    amount=amount,
                    status='successful'
                )
                return Response({
                    'message': 'Cash in successful',
                    'transaction': {
                        'timestamp':transaction_obj.timestamp.strftime('%Y-%m-%d %H:%M'),
                        'transaction_id':transaction_obj.transaction_id,
                        'wallet_number':transaction_obj.user.phone_number_wallet_number,
                        'type':'Cash In',
                        'amount':str(transaction_obj.amount),
                        'status':transaction_obj.status,
                    }
                },status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error':str(e)},status=status.HTTP_400_BAD_REQUEST)