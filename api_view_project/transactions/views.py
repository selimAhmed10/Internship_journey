from rest_framework.views import APIView
from .models import Transaction
from rest_framework.response import Response
from .serializers import TransactionSerializer
from django.shortcuts import get_object_or_404


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

