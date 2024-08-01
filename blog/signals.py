import json
import os

from blog.models import Blog, Author
from root import settings
from django.core.mail import send_mail
from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver


@receiver(pre_delete, sender=Blog)
def blog_pre_delete(sender, instance, **kwargs):
    directory = 'deleted/blogs'
    if not os.path.exists(directory):
        os.makedirs(directory)

    file_path = os.path.join(directory, f'{instance.title}_id_{instance.id}')
    data = {
        'id': instance.id,
        'title': instance.title,
        'content': instance.content,
        'date_added': str(instance.date_added),
        'auther_id': str(instance.auther_id),
        'category': str(instance.category),

    }

    try:
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
    except IOError as e:
        raise e


@receiver(pre_delete, sender=Author)
def author_pre_delete(sender, instance, **kwargs):
    directory = 'deleted/authors'
    if not os.path.exists(directory):
        os.makedirs(directory)

    file_path = os.path.join(directory, f'{instance.full_name}_id_{instance.id}')
    data = {
        'id': instance.id,
        'full_name': instance.full_name,
        'education': instance.education,
        'image': str(instance.image),

    }

    try:
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
    except IOError as e:
        raise e


@receiver(post_save, sender=Blog)
def blog_post_save(sender, instance, created, **kwargs):
    if created:
        print(f'{instance.title}_id_{instance.id} Successfully Created')
    else:
        print(f'{instance.title}_id_{instance.id} Successfully Updated')
