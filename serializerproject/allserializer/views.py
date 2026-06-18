from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User,Account,Transaction
from .serializers import BasicUserSerializer,AccountModelSerializer,UserHyperlinkSerializer
from django.shortcuts import get_object_or_404


class BasicUserAPIView(APIView):
    def get(self,request):
        users=User.objects.all()
        serializer=BasicUserSerializer(users,many=True)
        return Response(serializer.data)
    
    
    def post(self,request):
        serializer=BasicUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=201)
        return Response(serializer.error_messages("not suceessfull to craete the data"),status=400)

    def put(self,request,pk):
        user=get_object_or_404(User,pk=pk)
        serializer=BasicUserSerializer(user,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=201)
        return Response(serializer.errors,status=400)
    


class AccountModelSerializerAPIView(APIView):
    def get(self,request,pk=None):
        if pk:
            account= get_object_or_404(Account,pk=pk)
            serializer=AccountModelSerializer(account)
            return Response(serializer.data)
        
        accounts=Account.objects.all()
        serializer=AccountModelSerializer(accounts,many=True)
        return Response(serializer.data)
    
    
    def post(self,request):
        serializer=AccountModelSerializer(data=request.data)  # if here i use the many=true it will automatically craete the bulk amount of the data and in get use the many=True it will show list of many in background it will run the ListSerializer
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


    def put(self,request,pk):
        account=get_object_or_404(Account,pk=pk)
        serializer=AccountModelSerializer(account,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def patch(self,request,pk):
        account=get_object_or_404(Account,pk=pk)
        serializer=AccountModelSerializer(account,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk):
        account=get_object_or_404(Account,pk=pk)
        account.delete()
        return Response({"message":"deleted successfully"})
    
    

class UserListCreateAPIView(APIView):
    def get(self,request):
        users=User.objects.all()
        serializer=UserHyperlinkSerializer(users,many=True,context={'request':request})   #context help to create the full url using the info of the user 
        return Response(serializer.data)

    def post(self,request):
        serializer=UserHyperlinkSerializer(data=request.data,context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    
    
    

