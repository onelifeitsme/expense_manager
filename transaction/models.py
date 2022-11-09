from django.db import models
from django.db.models import Sum
from django.utils import timezone
import json


class Transaction(models.Model):
    user = models.ForeignKey('account.User', verbose_name='Пользователь', related_name='transactions', on_delete=models.CASCADE)
    amount = models.DecimalField(verbose_name='Сумма', max_digits=10, decimal_places=2, default=0.0)
    date = models.DateField(verbose_name='Дата', auto_now_add=True)
    time = models.TimeField(verbose_name='Время', auto_now_add=True)
    category = models.ForeignKey('TransactionCategory', related_name='transactions', on_delete=models.CASCADE)
    organization = models.CharField(verbose_name='Организация', max_length=255)
    description = models.CharField(verbose_name='Описание', max_length=255)

    def __str__(self):
        return f'{self.user}:{self.amount}'

    class Meta:
        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакции'


class TransactionCategory(models.Model):

    DEFAULT_CATEGORIES = ('Забота о себе', 'Зарплата', 'Здоровье и фитнес', 'Кафе и рестораны',
                          'Машина', 'Образование', 'Отдых и развлечения', 'Платежи, комиссии',
                          'Покупки: одежда, техника', 'Продукты', 'Проезд',)

    name = models.CharField(verbose_name='Название', max_length=255)
    user = models.ForeignKey('account.User', verbose_name='Пользователь', related_name='categories', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
