from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import (ListAPIView, ListCreateAPIView,
                                     RetrieveAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import IsAuthenticated

from api.serializers import (AccountSerializer, StatisticsCategorySerializer,
                             TransactionCategorySerializer,
                             TransactionSerializer)

from .filters import TransactionFilter


class AccountView(RetrieveAPIView):
    """Получение текущего баланса пользователя"""
    permission_classes = [IsAuthenticated]
    serializer_class = AccountSerializer

    def get_object(self):
        return self.request.user


class AccountStatisticsView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = StatisticsCategorySerializer

    def get_queryset(self, *args, **kwargs):
        days = self.request.query_params.get('days')
        return self.request.user.get_user_statistics(days)


class TransactionCategoryView(ListCreateAPIView):
    """Список категорий пользователя. Создание категории пользователем"""
    permission_classes = [IsAuthenticated]
    serializer_class = TransactionCategorySerializer

    def get_queryset(self):
        return self.request.user.categories.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SingleTransactionCategoryView(RetrieveUpdateDestroyAPIView):
    """Просмотр, изменение, удаление категории пользователя"""
    permission_classes = [IsAuthenticated]
    serializer_class = TransactionCategorySerializer

    def get_queryset(self):
        return self.request.user.categories.all()


class TransactionView(ListCreateAPIView):
    """Список транзакций пользователя. Создание транзакции пользователя"""
    permission_classes = [IsAuthenticated]
    serializer_class = TransactionSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TransactionFilter

    def get_queryset(self):
        return self.request.user.transactions.all()

    @transaction.atomic
    def perform_create(self, serializer):
        user = self.request.user
        amount = serializer.validated_data.get('amount')
        user.balance += amount
        user.save(update_fields=['balance'])
        serializer.save(user=user)
