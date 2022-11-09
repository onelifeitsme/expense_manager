from django.urls import path
from . import views


urlpatterns = [
    path('category/', views.TransactionCategoryView.as_view()),
    path('category/<int:pk>/', views.SingleTransactionCategoryView.as_view()),
    path('transaction/', views.TransactionView.as_view()),
    path('account/', views.AccountView.as_view()),
    path('account/statistics/', views.AccountStatisticsView.as_view()),
]