from __future__ import absolute_import

from django.core.mail import send_mail
from plugApps.celery import app
from celery import shared_task
import os
from plugApps import settings
from PIL import Image
from django.db import models
from django.db.models import signals


@app.task
def resize(input_image, size=(286, 180)):


    if not input_image or input_image == "":
        return

    name = input_image.replace('"','')

    print(name)
    image = Image.open(os.path.join(settings.MEDIA_ROOT, name))
    print(image)
    image = image.resize(size, Image.ANTIALIAS)

    image.save(os.path.join(settings.MEDIA_ROOT, name))


@app.task(name="send_confirmation_inscricao")
def send_confirmation_inscricao(first_name, last_name, titulo, email):


    subject = 'Nova Inscrição!'
    from_email = settings.EMAIL_HOST_USER
    message = f"""{first_name} {last_name} confirmou presença em {titulo}."""
    to = email

    send_mail(
        subject,
        message,
        from_email,
        [to],
        fail_silently=False,
    )
