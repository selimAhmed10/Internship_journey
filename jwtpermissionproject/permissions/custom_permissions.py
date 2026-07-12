from rest_framework.permissions import BasePermission
import jwt
from django.conf import settings

class RoleBasedPermission(BasePermission):
    allowed_roles=[]
    def has_permission(self, request, view):
        auth_header=request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return False
        
        token=auth_header.split(' ')[1]   #in token have three part 
                                            #first header 
                                            #second jti   that why take the index 1 after spilt 
                                            #signature 
        
        try:
            payload=jwt.decode(token,settings.SECRET_KEY,algorithms=['HS256'])
            user_role=payload.get('role')
            if not user_role:
                return False
            return user_role in self.allowed_roles
        except jwt.InvalidTokenError:
            return False

class IsAdmin(RoleBasedPermission):
    allowed_roles=['admin']

class IsAgent(RoleBasedPermission):
    allowed_roles=['agent']

class IsCustomer(RoleBasedPermission):
    allowed_roles=['customer']
      
class IsTransactionOwner(BasePermission):
    def has_object_permission(self,request,view,obj):
        if request.user.role=='admin':
            return True
        if request.user.role=='agent':
            return obj.agent==request.user or obj.user == request.user
        return obj.user==request.user or obj.to_user == request.user