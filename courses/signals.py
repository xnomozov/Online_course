import json
import os

from root import settings
from django.core.mail import send_mail
from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver

from courses.models import Course, User


@receiver(pre_delete, sender=Course)
def course_pre_delete(sender, instance, **kwargs):
    directory = 'deleted/customers'
    if not os.path.exists(directory):
        os.makedirs(directory)

    file_path = os.path.join(directory, f'{instance.title}_id_{instance.id}')
    data = {
        'id': instance.id,
        'title': instance.title,
        'description': instance.description,
        'number_of_students': instance.number_of_students,
        'duration': instance.duration,
        'teachers': str(instance.teachers),
        'rating': instance.rating,
        'image': str(instance.image),

    }

    try:
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
    except IOError as e:
        raise e


@receiver(post_save, sender=User)
def user_post_save(sender, instance, created, **kwargs):
    if created:
        pass
    else:
        subject = f'Hi {instance.username}'
        message = 'Your account has been added and saved successfully as user. Thank you! '
        email_from = settings.DEFAULT_FROM_EMAIL
        email_to = [instance.email]
        try:
            send_mail(subject, message, email_from, email_to, fail_silently=False)
            print(f'Email sent to {instance.email}')
        except Exception as e:
            raise f'Error sending email: {str(e)}'
