from CW_6_Django.celery import app
from clients.mail_sender import mail_send


@app.task
def mailing(period):
    mail_send(period=period)
    return "Done"

