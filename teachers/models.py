from django.db import models

from django.db import models


class Teacher(models.Model):
    class SpecializationChoices(models.TextChoices):
        BACKEND = 'Back-end'
        FRONTEND = 'Front-end'
        DESIGN = 'Graphic-Design'

    full_name = models.CharField(max_length=100)
    address = models.CharField(max_length=150, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(max_length=150, null=True, blank=True)
    rating = models.IntegerField(default=0, null=True, blank=True)
    specialization = models.CharField(
        max_length=20,
        choices=SpecializationChoices.choices,
        null=True,
        blank=True
    )
    image = models.ImageField(upload_to='teachers/', null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.full_name
