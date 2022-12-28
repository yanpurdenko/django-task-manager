# Generated by Django 4.1.4 on 2022-12-19 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='name',
            new_name='title',
        ),
        migrations.AlterField(
            model_name='position',
            name='name',
            field=models.CharField(choices=[('developer', 'Developer'), ('project manager', 'Project Manager'), ('designer', 'Designer'), ('devops', 'DevOps'), ('QA', 'QA')], max_length=255),
        ),
        migrations.AlterField(
            model_name='task',
            name='priority',
            field=models.CharField(choices=[('Critical', 'Critical'), ('Important', 'Important'), ('Normal', 'Normal'), ('Low', 'Low')], max_length=9),
        ),
        migrations.AlterField(
            model_name='tasktype',
            name='name',
            field=models.CharField(choices=[('Bug', 'Bug'), ('New Feature', 'New Feature'), ('Refactoring', 'Refactoring'), ('QA', 'QA')], max_length=255),
        ),
    ]
