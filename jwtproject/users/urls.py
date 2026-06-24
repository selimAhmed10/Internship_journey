from django.urls import path
from .views import UserResgisterAPIView,UserLoginAPIView,DashboardAPIView
urlpatterns = [
    path('register/',UserResgisterAPIView.as_view(),name='register'),
    path('login/',UserLoginAPIView.as_view(),name='login'),
    path('dashboard/',DashboardAPIView.as_view(),name='dashboard'),
]