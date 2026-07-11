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
