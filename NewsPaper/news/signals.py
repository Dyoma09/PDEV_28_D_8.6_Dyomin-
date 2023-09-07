from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from NewsPaper.settings import SITE_URL, DEFAULT_FROM_EMAIL
from .models import *
from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string
from django.contrib.auth.models import User, Group


# def send_notifications(preview, pk, title, subscribers):
#     html_context = render_to_string(
#         'post_created_email.html',
#         {
#             'text': preview,
#             'link': f'{SITE_URL}/news/{pk}'
#         }
#     )

#     msg = EmailMultiAlternatives(
#         subject=title,
#         body='',
#         from_email=DEFAULT_FROM_EMAIL,
#         to=subscribers,
#     )

#     msg.attach_alternative(html_context, 'text/html')
#     msg.send()

# @receiver(m2m_changed, sender=PostCategory)
# def notify_about_new_post(sender, instance, **kwargs):
#     if kwargs['action'] == 'post_add':
#         categories = instance.category.all()
#         subscribers: list[str] = []
#         for category in categories:
#             subscribers += category.subscribers.all()

#         subscribers = [s.email for s in subscribers]

#         send_notifications(instance.preview(), instance.pk, instance.title, subscribers)

@receiver(post_save, sender=User)
def add_user_to_common(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get('common')
        instance.groups.add(group)

@receiver(post_save, sender=User)
def send_confirmation_email(sender, instance, created, **kwargs):
    if created:
        subject = 'Подтверждение регистрации'
        name = User.objects.get('name')
        message = 'Здравствуйте, подтвердите ваш электронный ящик пройдя по ссылке:'
        send_mail(subject, message, [instance.email])