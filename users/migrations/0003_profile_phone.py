# Generated by Django 4.1.4 on 2023-01-15 14:41

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_remove_profile_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, help_text='Mobile phone number', max_length=128, region=None),
        ),
    ]
