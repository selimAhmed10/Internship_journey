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