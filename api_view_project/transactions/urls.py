from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import (TransactionAPIView,TransactionGenericView,TransactionModelViewSet)

router=DefaultRouter()
router.register('transactions',TransactionModelViewSet)

urlpatterns = [
    path('api/transactions/',TransactionAPIView.as_view()),
    path('api/transactions/<uuid:pk>/',TransactionAPIView.as_view()),

    path('api/generic/transactions/',TransactionGenericView.as_view()),
    path('api/generic/transactions/<uuid:pk>/',TransactionGenericView.as_view()),
    
    
    
    
    path('api/model/', include(router.urls)),
]