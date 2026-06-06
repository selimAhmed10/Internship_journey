from rest_framework.views import APIView
from .models import Account
from rest_framework.response import Response
from .serializers import AccountSerializer
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action

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
    
    
    
    
# Benefits of GenericAPIView  and Mixins
# Less code than APIView because CRUD operations come from built-in mixins(get,put,patch,delete etc)
# No need to write repetitive logic for list, create, retrieve, update and delete
# Here have build in queryset and serializer support makes the  code cleaner and easier to maintain and also make the operations
# Good for standard CRUD APIs when some or partial customization is needed
# Useful when APIView feels too manual but its do automatics with minimul code
# its much more easier than the APIView 


from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin,CreateModelMixin,DestroyModelMixin,RetrieveModelMixin,UpdateModelMixin     

class accountGenericView(GenericAPIView,CreateModelMixin,ListModelMixin,RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin):
    queryset=Account.objects.all()
    serializer_class=AccountSerializer
    
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
    

# Benefits of ModelViewSet
# Fastest and the easiest way to build full operations with minimum code
# Automatically provides list,create,retrieve,update and delete operations
# Works with routers(default and the simple routers) to generate URLs automatically
# Easy to maintain because all provide by the drf 
#Used to in productions because it easier to maintain 
# Least flexible of the three approaches but most productive and clean
# Best choice when custom logic or requirements are minimal and less 

from rest_framework.viewsets import ModelViewSet

class accountModelViewset(ModelViewSet):
    queryset=Account.objects.all()
    serializer_class=AccountSerializer
    


    @action(detail=True,methods=['post'])
    def freeze_account(self, request, pk=None):
        account=self.get_object()

        account.is_frozen=True
        account.save()

        return Response({
            "message":"Account frozen successfully",
            "account_number":account.account_number,
            "is_frozen":account.is_frozen
        })