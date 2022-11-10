from django.urls import path

from . import views

urlpatterns = [
    path('category/', views.TransactionCategoryView.as_view(), name='categories_list'),
    path('category/<int:pk>/', views.SingleTransactionCategoryView.as_view(), name='categories_detail'),
    path('transaction/', views.TransactionView.as_view(), name='transactions_list'),
    path('account/', views.AccountView.as_view(), name='account_detail'),
    path('account/statistics/', views.AccountStatisticsView.as_view(), name='account_statistics'),
]
