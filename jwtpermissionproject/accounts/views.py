from urllib import request
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from permissions.custom_permissions import IsAdmin
from .serializer import UserLoginSerializer,UserRegistrationSerializer,UserListSerializer,UserCreateSerializer,UserUpdateSerializer
from django.shortcuts import get_object_or_404

class UserResgistrationAPIView(APIView):
    permission_classes=[AllowAny]
    
    def post(self,request):
        userregistration=UserRegistrationSerializer(data=request.data)
        if userregistration.is_valid():
            user=userregistration.save()
            
            return Response({
                'message':" the user created successfully",
                'user':{
                    'id':str(user.id),
                    'username':user.username,
                    'role':user.role,
                    'email':user.email,
                    'full_name':user.full_name,
                }
            },status=status.HTTP_201_CREATED)
        return Response(userregistration.errors,status=status.HTTP_400_BAD_REQUEST)
            
class UserloginAPIView(APIView):
    permission_classes=[AllowAny]
    def post(self,request):
        loginserializer=UserLoginSerializer(data=request.data)
        if loginserializer.is_valid():
            user=loginserializer.validated_data['user']
            
            refresh=RefreshToken.for_user(user)
            access=refresh.access_token
            refresh['role']=user.role 
            access['role']=user.role
            
            return Response({
                'access':str(access),
                'refresh':str(refresh),
                'user':{
                    'id':str(user.id),
                    'username':user.username,
                    'role':user.role,
                }
            },status=status.HTTP_200_OK)
        return Response(loginserializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
class LogOutAPIview(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        try:
            refresh_token=request.data.get('refresh')
            if refresh_token:
                token=RefreshToken(refresh_token)
                token.blacklist()
            return Response({'message':"Logout successfully"})
        except Exception as e:
            return Response({'error':str(e)},status=status.HTTP_400_BAD_REQUEST)
        
        
        
class AdminUserListView(APIView):
    permission_classes=[IsAdmin]
    def get(self,request):
        users=User.objects.all().order_by('-created_at')
        serializer=UserListSerializer(users,many=True)
        return Response(serializer.data)


class UserManageView(APIView):
    permission_classes=[IsAdmin]
    def get(self,request,user_id=None):
        if user_id:
            user=get_object_or_404(User,id=user_id)
            serializer=UserListSerializer(user)
            return Response(serializer.data)
        
        users=User.objects.all().order_by('-created_at')
        serializer=UserListSerializer(users,many=True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer=UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.save()
            return Response({'message':'User created successfully','user':UserListSerializer(user).data},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def put(self,request,user_id):
        user=get_object_or_404(User,id=user_id)
        serializer = UserUpdateSerializer(user, data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'User updated successfully','user': UserListSerializer(user).data})
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, user_id):
        user=get_object_or_404(User,id=user_id)
        user.delete()
        return Response({'message':'User deleted successfully'},status=status.HTTP_200_OK)