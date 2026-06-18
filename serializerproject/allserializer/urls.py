from django.urls import path
from .views import BasicUserAPIView,AccountModelSerializerAPIView,UserListCreateAPIView
from .views import ReadOnlyTransaction,AccountComputedDetails,AccountMoneyMaskedApiView,UserRegistrationAPIView,TransactionNastedReadAPIView,TransactionWriteNastedAPIView

urlpatterns=[

    # Basic Serializer
    path("user/",BasicUserAPIView.as_view()),  # GET all users,create user
    path("user/<int:pk>/",BasicUserAPIView.as_view()), # PUT update user

    # Model Serializer
    path("account/",AccountModelSerializerAPIView.as_view()),  # GET all,create
    path("account/<int:pk>/",AccountModelSerializerAPIView.as_view()),#put,patch,delete by id 

    # Hyperlinked Serializer
    path("hyper/user/",UserListCreateAPIView.as_view()), # get and create 

    # Read only Transaction Serializer
    path("readonly/transaction/",ReadOnlyTransaction.as_view()), #get all
    path("readonly/transaction/<int:pk>/",ReadOnlyTransaction.as_view()),#get one by id 

    # Computed Fields
    path("computed/account/<int:pk>/",AccountComputedDetails.as_view()),  # Serializer method field for getting new field available balance , total transaction and the last active(amount)

    # Custom Fields(money field and masked account)
    path("custom/account/",AccountMoneyMaskedApiView.as_view()),    #get all
    path("custom/account/<int:pk>/",AccountMoneyMaskedApiView.as_view()),  # get one by id

    # user registration
    path("register/user/", UserRegistrationAPIView.as_view()),

    # Nested Read Serializer
    path("nested/read/transaction/",TransactionNastedReadAPIView.as_view()),# read all
    path("nested/read/transaction/<int:pk>/",TransactionNastedReadAPIView.as_view()),#read one

    # Writable Nested Serializer
    path("nested/write/transaction/",TransactionWriteNastedAPIView.as_view()),  #post 
    path("nested/write/transaction/<int:pk>/",TransactionWriteNastedAPIView.as_view()),  #update (full and partial)
]