from django.urls import path
from .views import UserResgisterAPIView,UserLoginAPIView,DashboardAPIView,LogOutAPIView,TokenRefreshAPIView
urlpatterns = [
    path('register/',UserResgisterAPIView.as_view(),name='register'),
    path('login/',UserLoginAPIView.as_view(),name='login'),
    path('dashboard/',DashboardAPIView.as_view(),name='dashboard'),
    path('refresh_token/',TokenRefreshAPIView.as_view(),name='refresh_rotation'),
    path('logout/',LogOutAPIView.as_view(),name='logout')
]