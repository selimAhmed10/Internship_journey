from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User,Account,Transaction
from .serializers import BasicUserSerializer
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
        
        
     