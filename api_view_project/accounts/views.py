from rest_framework.views import APIView
from .models import Account
from rest_framework.response import Response
from .serializers import AccountSerializer
from django.shortcuts import get_object_or_404

# Benefits of APIView
#Full control over every request and response(can modify logic exactly as needed or want,no dependency have on buold drf shortcart)
#Can write custom business logic easily as per developer requirement
#Flexible and easier for complex or unique API behavior(work individual urls to do operations)
#Use- Good for learning how DRF works internally and when need custom logic 
#Useful when each endpoint needs different behavior to perform but its need to write every line code


class AccountAPIView(APIView):
    def get(self,request,pk=None):
        if pk:
            account = get_object_or_404(Account, pk=pk)
            serializer=AccountSerializer(account)
            return Response(serializer.data)

        accounts=Account.objects.all()
        serializer=AccountSerializer(accounts,many=True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer=AccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def put(self,request,pk):
        account = get_object_or_404(Account, pk=pk)
        serializer=AccountSerializer(account,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def patch(self,request,pk):
        account = get_object_or_404(Account, pk=pk)
        serializer=AccountSerializer(account,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def delete(self,request,pk):
        account = get_object_or_404(Account, pk=pk)
        account.delete()
        return Response({"message":"successfully deleted"})
        