from celery import shared_task
from django.template.loader import render_to_string
from django.urls import reverse
from django.core.mail import send_mail
from .models import Respond
from django.conf import settings
from urllib.parse import urljoin


@shared_task
def notify_about_new_respond(respond_id):
    respond = Respond.objects.get(id=respond_id)
    announcement = respond.announcement
    user = announcement.user

    respond_url = urljoin(settings.BASE_URL, reverse('respond_detail', kwargs={'pk': respond.id}))
            
    html_message = render_to_string('notify/notify_about_new_respond.html', {
        'title': f'Новый отклик на {announcement.header}',
        'text': respond.text,
        'post_url': respond_url  
        })
            
    send_mail(
        subject=f'Новый отклик на {announcement.header}',
        message='',
        html_message=html_message,
        recipient_list=[user.email],
        from_email=settings.DEFAULT_FROM_EMAIL,
        fail_silently=False,
        )
    
    
@shared_task
def notify_about_accepted_respond(respond_id):
    respond = Respond.objects.get(id=respond_id)
    announcement = respond.announcement
    user = respond.user 

    respond_url = urljoin(settings.BASE_URL, reverse('respond_detail', kwargs={'pk': respond.id}))

    html_message = render_to_string('notify/respond_accepted_email.html', {
        'announcement': announcement,
        'respond': respond,
        'user': user,
        'respond_url': respond_url,
    })

    send_mail(
        subject=f'Ваш отклик на "{announcement.header}" принят!',
        message='',
        html_message=html_message,
        recipient_list=[user.email],
        from_email=settings.DEFAULT_FROM_EMAIL,
        fail_silently=False,
    )