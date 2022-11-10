from django.contrib import admin

from transaction.models import Transaction, TransactionCategory

admin.site.register(Transaction)
admin.site.register(TransactionCategory)
