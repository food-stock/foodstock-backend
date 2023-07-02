from django.core.mail import send_mail

def send_email(to, subject, message):
    send_mail(
        subject,
        message,
    'from@example.com',
    [to],
    fail_silently=False,
    )