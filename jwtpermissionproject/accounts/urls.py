from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import UserloginAPIView,UserResgistrationAPIView,LogOutAPIview
urlpatterns=[
    path('register/', UserResgistrationAPIView.as_view(),name='register'),
    path('login/', UserloginAPIView.as_view(),name='login'),
    path('refresh/', TokenRefreshView.as_view(),name='token_refresh'),
    path('logout/', LogOutAPIview.as_view(),name='logout'),
]