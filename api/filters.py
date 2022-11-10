from django_filters import (DateFromToRangeFilter, FilterSet, NumberFilter,
                            TimeRangeFilter)

from transaction.models import Transaction


class TransactionFilter(FilterSet):
    amount = NumberFilter(field_name='amount', label='Точная сумма')
    amount_min = NumberFilter(field_name='amount', label='Сумма от', lookup_expr='gte')
    amount_max = NumberFilter(field_name='amount', label='Сумма до', lookup_expr='lte')
    date = DateFromToRangeFilter(field_name='date', label='Дата от-до')
    time = TimeRangeFilter(field_name='time', label='Время от-до')

    class Meta:
        model = Transaction
        fields = ['amount', 'amount_min', 'amount_max', 'date', 'time']
