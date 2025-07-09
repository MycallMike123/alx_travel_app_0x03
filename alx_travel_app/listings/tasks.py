from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_booking_email(recipient_email, booking_info):
    subject = 'Booking Confirmation'
    message = f'Your booking is confirmed:\n\n{booking_info}'
    send_mail(subject, message, None, [recipient_email])

