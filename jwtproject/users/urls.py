from django.urls import path
from .views import UserResgisterAPIView,UserLoginAPIView,DashboardAPIView,LogOutAPIView,TokenRefreshAPIView
from .views import RevokeSessionAPIView,RevokeAllSessionsAPIView,ActiveSessionAPIView
urlpatterns = [
    path('register/',UserResgisterAPIView.as_view(),name='register'),
    path('login/',UserLoginAPIView.as_view(),name='login'),
    path('dashboard/',DashboardAPIView.as_view(),name='dashboard'),
    path('refresh_token/',TokenRefreshAPIView.as_view(),name='refresh_rotation'),
    path('logout/',LogOutAPIView.as_view(),name='logout'),
    path('sessions/',ActiveSessionAPIView.as_view(),name='active_sessions'),
    path('sessions/revoke/<str:session_id>/',RevokeSessionAPIView.as_view(), name='revoke_session'),
    path('sessions/revoke_all/',RevokeAllSessionsAPIView.as_view(),name='revoke_all_sessions'),
]