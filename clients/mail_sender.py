from datetime import datetime

from django.core.mail import send_mail

from CW_6_Django import settings
from clients.models import Newsletter, Log


def mail_send(period=None, newsletters=None):
    if not period and not Newsletter:
        return None
    if not newsletters:
        newsletters = Newsletter.objects.filter(period=period)
    for newsletter in newsletters:  # перебираем каждую
        messages = newsletter.messages.all()  # получаем список сообщений для этой рассылки
        newsletter.status = Newsletter.STATUS_STARTED
        newsletter.save()
        for client in newsletter.client.filter(is_blocked=False):  # перебираем всех пользователей этой рассылки
            for message in messages:  # перебираем все сообщения для этой рассылки
                try:
                    Log.objects.create(  # логи о начале отправки
                        date_attempt=datetime.now(),
                        state=Newsletter.STATUS_STARTED,
                        response_server="200",
                        message=message
                    )
                    send_mail(  # делаем рассылку
                        subject=message.theme,
                        message=message.letter,
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[client.email],
                    )
                    Log.objects.create(  # логи о завершении отправки
                        date_attempt=datetime.now(),
                        state=Newsletter.STATUS_DONE,
                        response_server="200",
                        message=message
                    )
                except Exception as e:  # если произошла ошибка при отправке
                    Log.objects.create(
                        date_attempt=datetime.now(),
                        state='1',
                        response_server=str(e),
                        message=message
                    )
        newsletter.status = Newsletter.STATUS_DONE
        newsletter.save()
