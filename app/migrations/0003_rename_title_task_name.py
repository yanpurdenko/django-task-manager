# Generated by Django 4.1.4 on 2022-12-19 18:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_rename_name_task_title_alter_position_name_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='title',
            new_name='name',
        ),
    ]
