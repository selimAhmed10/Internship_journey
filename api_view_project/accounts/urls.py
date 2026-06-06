from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AccountAPIView,accountGenericView,accountModelViewset

router=DefaultRouter()
router.register('accounts',accountModelViewset)

urlpatterns=[
    # APIView
    path('api/api/accounts/',AccountAPIView.as_view()),  #get all and craete
    path('api/api/accounts/<uuid:pk>/',AccountAPIView.as_view()),  #all operations using the pk(id)
    
    #GenericAPIView with all Mixins
    path('api/generic/accounts/',accountGenericView.as_view()),                
    path('api/generic/accounts/<uuid:pk>/',accountGenericView.as_view()),     
    
    #ModelViewSet 
    path('api/model/',include(router.urls)),                                 
]