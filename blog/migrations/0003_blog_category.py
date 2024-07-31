# Generated by Django 5.0.7 on 2024-07-31 07:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_remove_author_age_remove_blog_auther_id_and_more'),
        ('courses', '0004_alter_video_video'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='category',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, to='courses.category'),
            preserve_default=False,
        ),
    ]
