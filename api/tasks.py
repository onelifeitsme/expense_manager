from celery import shared_task
from django.template.loader import render_to_string
from account.models import User
from django.core.mail import EmailMessage, send_mail
from django.conf import settings


@shared_task
def send_statistics_to_users():
    """Функция отправки письма со статистикой расходов всем пользователям"""
    send_mail(
        subject='Статистика расходов',
        message='вапвапвап вапва пвап вап вап ',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email for user in User.objects.all()],
        fail_silently=False,
    )