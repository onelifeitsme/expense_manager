import json
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView, ListAPIView
from django.contrib.auth import get_user_model
from api.serializers import AccountSerializer, StatisticsCategorySerializer, TransactionSerializer, TransactionCategorySerializer
from django.db import transaction
from rest_framework.views import APIView
from transaction.models import Transaction, TransactionCategory
from django_filters.rest_framework import DjangoFilterBackend
from .filters import TransactionFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


User = get_user_model()


class AccountView(RetrieveAPIView):
    """Получение текущего баланса пользователя"""
    serializer_class = AccountSerializer

    def get_object(self):
        return self.request.user


class AccountStatisticsView(ListAPIView):
    serializer_class = StatisticsCategorySerializer

    def get_queryset(self, *args, **kwargs):
        days = self.request.query_params.get('days')
        return User.objects.last().get_user_statistics(days)


class TransactionCategoryView(ListCreateAPIView):
    """Список категорий пользователя. Создание категории пользователем"""
    serializer_class = TransactionCategorySerializer

    def get_queryset(self):
        return self.request.user.categories.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SingleTransactionCategoryView(RetrieveUpdateDestroyAPIView):
    """Просмотр, изменение, удаление категории пользователя"""
    serializer_class = TransactionCategorySerializer

    def get_queryset(self):
        return self.request.user.categories.all()


class TransactionView(ListCreateAPIView):
    """Список транзакций пользователя. Создание транзакции пользователя"""
    serializer_class = TransactionSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TransactionFilter


    def get_queryset(self):
        # return self.request.user.transactions.all()
        return Transaction.objects.all()

    @transaction.atomic
    def perform_create(self, serializer):
        user = self.request.user
        amount = serializer.validated_data.get('amount')
        user.balance += amount
        user.save(update_fields=['balance'])
        serializer.save(user=user)




