import os
import smtplib
import ssl

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)


@receiver(post_save, sender=Book)
def send_email(sender, instance, **kwargs):
    port = 465  # For SSL
    sender_email = os.getenv('SENDER_EMAIL')
    receiver_email = get_user_model().objects.get(pk=instance.user_id).email
    sender_password = os.getenv('SENDER_PASSWORD')
    message = """\
            Subject: BookClub

            A new Book had been added into the database"""

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message)
















