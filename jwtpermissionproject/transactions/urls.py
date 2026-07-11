from django.urls import path
from .views import *

urlpatterns = [
    path('admin/dashboard/',AdminDashboard.as_view(),name='admin_dashboard'),
    path('admin/transactions/',AdminAllTransactionsView.as_view(),name='admina_ll_transactions'),
    path('agent/dashboard/',AgentDashboard.as_view(), name='agent_dashboard'),
    path('agent/transactions/',AgentTransaction.as_view(),name='agent_transactions'),
    path('agent/cash-in/',CashIn.as_view(),name='agent_cash_in'),
    path('customer/dashboard/',CustomerDashboardView.as_view(),name='customer_dashboard'),
    path('customer/transactions/',CustomerTransactions.as_view(), name='customer_transactions'),
    path('customer/send-money/',CustomerSendMoneyView.as_view(), name='customer_send-money'),
    path('customer/cash-out/',CustomerCashOut.as_view(), name='customer_cash_out'),
]