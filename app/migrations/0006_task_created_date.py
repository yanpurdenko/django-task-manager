# Generated by Django 4.1.4 on 2022-12-22 21:40

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_remove_task_task_type_task_task_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='created_date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
