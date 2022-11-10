from rest_framework import serializers

from account.models import User
from transaction.models import Transaction, TransactionCategory


class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('balance',)


class TransactionCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = TransactionCategory
        fields = ('name',)


class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        exclude = ('user',)


class StatisticsCategorySerializer(serializers.Serializer):
    category = serializers.CharField()
    result = serializers.DecimalField(max_digits=10, decimal_places=2, allow_null=True)
