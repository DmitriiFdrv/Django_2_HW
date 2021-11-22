from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings


def send_verify_mail(user):
    verify_link = reverse('auth:verify', args=[user.email, user.activation_key])
    full_link = f'{settings.BASE_URL}{verify_link}'

    message = f'your activation URL: {full_link}'

    return send_mail(
        'Account activation',
        message,
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False
    )