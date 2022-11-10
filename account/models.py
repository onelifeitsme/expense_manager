from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.db.models import Sum
from django.utils import timezone

from transaction.models import TransactionCategory


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('email', unique=True, null=True)
    date_joined = models.DateTimeField('Дата регистрации', auto_now_add=True, null=True, blank=True)
    is_staff = models.BooleanField('Сотрудник', default=False)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_user_statistics(self, days=1, special_day=None):
        """Статистика по категориям пользователя с выбираeмым количеством дней"""
        data = []
        user_categories = self.categories.all().prefetch_related('transactions')
        if special_day:
            date_range = [special_day, special_day]
        else:
            date_range = [timezone.now() - timezone.timedelta(days=int(days or 1) - 1), timezone.now()]
        for category in user_categories:
            category_transactions = category.transactions.filter(date__range=date_range)
            data.append(
                {
                    'category': category.name,
                    'result': category_transactions.aggregate(sum=Sum('amount')).get('sum'),
                }
            )
        return data

    def save(self, *args, **kwargs):
        if not getattr(self, 'date_joined'):
            super().save(*args, **kwargs)
            for category in TransactionCategory.DEFAULT_CATEGORIES:
                TransactionCategory.objects.create(name=category, user=self)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
