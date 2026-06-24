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


class UserLoginAPIView(APIView):
    permission_classes=[AllowAny]  #everyrole and anyone can try login using the email and the password 
    def post(self,request):
        serializer=UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            data=serializer.validated_data 
            return Response({
                "status":"success",
                "message":"User login successfull",
                "data": {
                    "user": {
                        "id":str(data["user"].id), # receive the data from the serializer and access it to show user info
                        "email":data["user"].email,
                        "role":data["user"].role
                    },
                    "access":data["access"],  # access and refrsh token create in the serializer class here just access and return it to the user 
                    "refresh":data["refresh"]
                }
            },status=status.HTTP_200_OK)
        return Response(serializer.errors)
     