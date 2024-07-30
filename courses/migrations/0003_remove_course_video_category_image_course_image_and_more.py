# Generated by Django 5.0.7 on 2024-07-30 13:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_course_rating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='video',
        ),
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(default=1, upload_to='images/'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='course',
            name='image',
            field=models.ImageField(default=2, upload_to='images/'),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=299)),
                ('video', models.FileField(upload_to='videos/')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='videos', to='courses.course')),
            ],
        ),
    ]
