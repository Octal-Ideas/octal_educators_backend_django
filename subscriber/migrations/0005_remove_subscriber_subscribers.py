# Generated by Django 4.2.2 on 2023-06-22 13:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subscriber', '0004_subscriber_subscribers'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscriber',
            name='subscribers',
        ),
    ]
