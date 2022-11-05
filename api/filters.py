from django_filters import FilterSet, AllValuesFilter
from django_filters import DateTimeFilter, NumberFilter, RangeFilter, DateFromToRangeFilter, TimeRangeFilter
from transaction.models import Transaction


class TransactionFilter(FilterSet):
    amount = RangeFilter()
    date = DateFromToRangeFilter()
    time = TimeRangeFilter()


    class Meta:
        model = Transaction
        fields = ['amount', 'date', 'time']