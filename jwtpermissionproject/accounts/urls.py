from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import AdminUserListView, UserManageView, UserloginAPIView,UserResgistrationAPIView,LogOutAPIview
urlpatterns=[
    path('register/', UserResgistrationAPIView.as_view(),name='register'),
    path('login/', UserloginAPIView.as_view(),name='login'),
    path('refresh/',TokenRefreshView.as_view(),name='token_refresh'),
    path('logout/', LogOutAPIview.as_view(),name='logout'),
    path('admin/users/list/',AdminUserListView.as_view(), name='admin-users-list'),
    path('admin/users/', UserManageView.as_view(), name='admin-users'),
    path('admin/users/<uuid:user_id>/', UserManageView.as_view(), name='admin-user-detail'),
]