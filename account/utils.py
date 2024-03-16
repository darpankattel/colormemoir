# from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string

import random
from django.utils import timezone
from .models import OTP


# @shared_task
def send_mail(data):
    subject = data.get('subject')
    template = data.get('template')
    to = data.get('to')
    text = ""

    reply_to = settings.EMAIL_REPLY_TO_USER
    from_email = settings.EMAIL_HOST_USER
    html_content = render_to_string(template, data)

    mail = EmailMultiAlternatives(subject, text, from_email, to,
                                  reply_to=[reply_to, ])
    mail.attach_alternative(html_content, "text/html")
    try:
        mail.send(fail_silently=False)
        return True
    except Exception as e:
        pass
        raise
        # return False

    return True


def generate_otp(length=6):
    return ''.join(str(random.randint(0, 9)) for _ in range(length))


def save_otp(user):
    otp_instance, created = OTP.objects.get_or_create(user=user)
    if otp_instance.expired:
        otp_instance.otp = generate_otp()
        otp_instance.created = timezone.now()
    otp_instance.save()
    return otp_instance.otp


def verify_otp(user, otp_input):
    try:
        otp_instance = OTP.objects.get(user=user)
        if otp_instance.otp == otp_input and not otp_instance.expired:
            return True
    except OTP.DoesNotExist:
        return False

    return False
