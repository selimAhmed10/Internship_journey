from datetime import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework import status
from .serializers import UserRegisterSerializer,UserLoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from .models import UserSession


def get_session_info(request):   #get the user session information ip,browser,device 
    x_forward_for=request.META.get('HTTP_X_FORWARD_FOR')
    if x_forward_for:
        ip=x_forward_for.split(',')[0].strip()
    else:
        ip=request.META.get('REMOTE_ADDR','unknown_ip')
    user_agent= request.META.get('HTTP_USER_AGENT','Unknown Browser')
    if 'Windows' in user_agent:
        device='Windows PC'
    elif 'Macintosh' in user_agent:
        device='Mac'
    elif 'iPhone' in user_agent:
        device='iPhone'
    elif 'Android' in user_agent:
        device='Android Phone'
    elif 'iPad' in user_agent:
        device='iPad'
    else:
        device='Unknown Device'

    if 'Chrome' in user_agent and 'Edg' not in user_agent:
        browser='Chrome'
    elif 'Firefox' in user_agent:
        browser='Firefox'
    elif 'Safari' in user_agent and 'Chrome' not in user_agent:
        browser='Safari'
    elif 'Edg' in user_agent:
        browser='Edge'
    else:
        browser='Unknown Browser'
    
    return {'ip':ip,'user_agent':user_agent,'device':device,'browser':browser}


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
            user=data['user']   #from the data find the user
            session_info=get_session_info(request)#call get function to get the info of device,ip,browser,useragents
            session=UserSession.objects.create(  #create the sessin using the login info
                user=user,
                access_token_jti=data['access_jti'],      
                refresh_token_jti=data['refresh_jti'], 
                device_name=session_info['device'],
                browser_name=session_info['browser'],
                ip_address=session_info['ip'],
                user_agent=session_info['user_agent'],
                expires_at=timezone.now()+timezone.timedelta(days=7),
                is_active=True
            )

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
                    "refresh":data["refresh"],
                    "session_id":str(session.session_id)  #pass the sesssion id 
                }
            },status=status.HTTP_200_OK)
        return Response(serializer.errors)
    
    
class DashboardAPIView(APIView):   # need to request using the access token then it extract then do check with user info,expire,blacklist or not after all return the user info it okey 
    permission_classes=[IsAuthenticated]  # only authenticate user can access this page using their access token 

    def get(self,request):
        user=request.user  # trac witch user trying to access and find out 
        return Response({
            "status":"success",
            "message":f"Welcome {user.email}",
            "data":{
                "user":{
                    "id":str(user.id),
                    "email":user.email,
                    "name":user.name,
                    "role":user.role
                }
            }
        },status=status.HTTP_200_OK)
        

class TokenRefreshAPIView(APIView):
    permission_classes=[AllowAny]
    def post(self,request):
        old_refresh_token=request.data.get('refresh')  # receive the refresh token as old 
        if not old_refresh_token:  #check refresh have or not 
            return Response({
                "status":"error",
                "message":"Refresh token is need not here"
            },status=status.HTTP_400_BAD_REQUEST)
     
        try:
            refresh=RefreshToken(old_refresh_token)  #from the old fresh make a new refresh token 
            user_id=refresh.payload.get('user_id') # get the user 
            new_access_token=refresh.access_token  #create new access token by just calling 
            new_refresh_token=str(refresh)   # token rotation ( true in the settings)
            #after done make the old in blacklist  after rotation blacklist true in settings 
            return Response({
                "status":"success",
                "message":"Token refreshed successfully",
                "data":{
                    "user_id":user_id,
                    "access":str(new_access_token),
                    "refresh":new_refresh_token,
                }
            },status=status.HTTP_200_OK)
            
        except TokenError as e:
            return Response({
                "status":"error",
                "message":f"Invalid refresh token:{str(e)}"
            },status=status.HTTP_401_UNAUTHORIZED)




class LogOutAPIView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        refresh_token=request.data.get('refresh')
        if not refresh_token:  #check refresh have or not 
            return Response({
                "status":"error",
                "message":"Refresh token is need not here"
            },status=status.HTTP_400_BAD_REQUEST)
        
        try:
            refresh=RefreshToken(refresh_token)   # make it python object to check everything , user check,expire and others
            refresh.blacklist()  # then block the refresh because its timeline huge 
            return Response({
                "status":"success",
                "message":"Log out out successfully"
            }, status=status.HTTP_200_OK)
            
        except TokenError as e:
            return Response({
                "status":"error",
                "message":f"Invalid refresh token:{str(e)}"
            }, status=status.HTTP_400_BAD_REQUEST)
