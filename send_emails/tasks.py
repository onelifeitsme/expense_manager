from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone

from account.models import User


@shared_task
def send_statistics_to_users():
    """Функция отправки письма со статистикой расходов всем пользователям"""
    for user in User.objects.all():
        user_yesterday_statistics = user.get_user_statistics(special_day=timezone.now() - timezone.timedelta(days=1))
        send_mail(
            subject='Статистика расходов',
            message='',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
            html_message=render_to_string('send_emails/statistics_email.html',
                                          context={'user_yesterday_statistics': user_yesterday_statistics}))
