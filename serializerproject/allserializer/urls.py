from django.urls import path
from .views import BasicUserAPIView,AccountModelSerializerAPIView,UserListCreateAPIView
from .views import ReadOnlyTransaction,AccountComputedDetails,AccountMoneyMaskedApiView,UserRegistrationAPIView,TransactionNastedReadAPIView,TransactionWriteNastedAPIView

urlpatterns=[

    # Basic Serializer
    path("api/user/",BasicUserAPIView.as_view()),  # GET all users,create user
    path("api/user/<int:pk>/",BasicUserAPIView.as_view()), # PUT update user

    # Model Serializer
    path("api/account/",AccountModelSerializerAPIView.as_view()),  # GET all,create
    path("api/account/<int:pk>/",AccountModelSerializerAPIView.as_view()),#put,patch,delete by id 

    # Hyperlinked Serializer
    path("api/hyper/user/",UserListCreateAPIView.as_view()), # get and create 

    # Read only Transaction Serializer
    path("api/readonly/transaction/",ReadOnlyTransaction.as_view()), #get all
    path("api/readonly/transaction/<int:pk>/",ReadOnlyTransaction.as_view()),#get one by id 

    # Computed Fields
    path("api/computed/account/<int:pk>/",AccountComputedDetails.as_view()),  # Serializer method field for getting new field available balance , total transaction and the last active(amount)

    # Custom Fields(money field and masked account)
    path("api/custom/account/",AccountMoneyMaskedApiView.as_view()),    #get all
    path("api/custom/account/<int:pk>/",AccountMoneyMaskedApiView.as_view()),  # get one by id

    # user registration
    path("api/register/user/", UserRegistrationAPIView.as_view()),

    # Nested Read Serializer
    path("api/nested/read/transaction/",TransactionNastedReadAPIView.as_view()),# read all
    path("api/nested/read/transaction/<int:pk>/",TransactionNastedReadAPIView.as_view()),#read one

    # Writable Nested Serializer
    path("api/nested/write/transaction/",TransactionWriteNastedAPIView.as_view()),  #post 
    path("api/nested/write/transaction/<int:pk>/",TransactionWriteNastedAPIView.as_view()),  #update (full and partial)
]