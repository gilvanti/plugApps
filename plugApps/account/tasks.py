from celery.utils.log import get_task_logger
from django.conf import settings
from django.core.mail import send_mail

from plugApps.celery import app

logger = get_task_logger(__name__)


@app.task(name="send_confirmation_email_task")
def send_confirmation_email(token, id, email):

    subject = 'Obrigado por se cadastrar!'
    from_email = settings.EMAIL_HOST_USER
    message = f"http://localhost:8000/account/confirm/?confirmation_key={token}&id={id}"
    to = email

    send_mail(
        subject,
        message,
        from_email,
        [to],
        fail_silently=False,
    )
