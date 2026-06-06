from rest_framework.views import APIView
from .models import Transaction
from rest_framework.response import Response
from .serializers import TransactionSerializer
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action


class TransactionAPIView(APIView):
    def get(self,request,pk=None):
        if pk:
            transaction=get_object_or_404(Transaction,pk=pk)
            serializer=TransactionSerializer(transaction)
            return Response(serializer.data)

        transactions=Transaction.objects.all()
        serializer=TransactionSerializer(transactions,many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer=TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def put(self,request,pk):
        transaction=get_object_or_404(Transaction,pk=pk)
        serializer=TransactionSerializer(transaction, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def patch(self,request,pk):
        transaction=get_object_or_404(Transaction,pk=pk)
        serializer=TransactionSerializer(transaction,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def delete(self,request,pk):
        transaction=get_object_or_404(Transaction,pk=pk)
        transaction.delete()
        return Response({"message": "successfully deleted"})



from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin,CreateModelMixin,DestroyModelMixin,RetrieveModelMixin,UpdateModelMixin

class TransactionGenericView(GenericAPIView,CreateModelMixin,ListModelMixin,RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin):
    queryset=Transaction.objects.all()
    serializer_class=TransactionSerializer

    def get(self,request,pk=None):
        if pk:
            return self.retrieve(request,pk=pk)
        return self.list(request)

    def post(self,request):
        return self.create(request)

    def put(self,request,pk):
        return self.update(request,pk=pk)

    def patch(self,request,pk):
        return self.partial_update(request,pk=pk)

    def delete(self,request,pk):
        return self.destroy(request,pk=pk)
  
  
    
from rest_framework.viewsets import ModelViewSet

class TransactionModelViewSet(ModelViewSet):
    queryset=Transaction.objects.all()
    serializer_class=TransactionSerializer
    
    #Get the transaction status
    @action(detail=True,methods=['get'])
    def status(self,request,pk=None):
       
        transaction=self.get_object()
        return Response({
            'transaction_id':str(transaction.trans_id),
            'status':transaction.status,
            'amount':transaction.amount,
            'type':transaction.transaction_type,
            'created_at':transaction.created_at,
            'account_number': transaction.account.account_number,
        })
        
    @action(detail=True,methods=['post'])
    def reverse(self,request,pk=None):
        transaction=self.get_object()

    # create reversed transaction
        reversed_transaction=Transaction.objects.create(
            account=transaction.account,
            amount=transaction.amount,
            transaction_type='credit' if transaction.transaction_type== 'debit' else 'debit',
            status='reversed'
            )

        # update the  original transaction
        transaction.status ='reversed'
        transaction.save()

        return Response({
            "message":"reversed successfully",
            "original":str(transaction.trans_id),
            "reversed":str(reversed_transaction.trans_id)
        })