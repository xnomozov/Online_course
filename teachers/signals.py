import json
import os

from root import settings

from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver

from teachers.models import Teacher
#
#
@receiver(pre_delete, sender=Teacher)
def teachers_pre_delete(sender, instance, **kwargs):
    directory = 'deleted/teachers'
    if not os.path.exists(directory):
        os.makedirs(directory)

    file_path = os.path.join(directory, f'{instance.full_name}_id_{instance.id}')
    data = {
        'id': instance.id,
        'full_name': instance.full_name,
        'specialization': str(instance.specialization),
        'description': instance.description,
        'level': str(instance.level),
        'rating': instance.rating,
        'image': str(instance.image),

    }

    try:
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
    except IOError as e:
        raise e


@receiver(post_save, sender=Teacher)
def teacher_post_save(sender, instance, created, **kwargs):
    if created:
        print(f'{instance.full_name}_id_{instance.id} Successfully Created')
    else:
        print(f'{instance.full_name}_id_{instance.id} Successfully Updated')
