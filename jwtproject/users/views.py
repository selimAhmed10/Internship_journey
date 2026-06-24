from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework import status
from .serializers import UserRegisterSerializer,UserLoginSerializer

class UserResgisterAPIView(APIView):
    
    permission_classes=[AllowAny]  # anyone can do login 
    def post(self,request):
        register_serializer=UserRegisterSerializer(data=request.data)
        if register_serializer.is_valid():
            user=register_serializer.save()
       
            return Response({
                "status":"success",
                "message":"User successfully created",
                "data":{
                    "id":str(user.id),
                    "email":user.email,
                    "phone":user.phone,
                    "address":user.address,
                    "role":user.role
                }
            },status=status.HTTP_201_CREATED)
        return Response(register_serializer.errors)  
