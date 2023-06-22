# Generated by Django 4.2.2 on 2023-06-20 06:32

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('subscriber', '0002_remove_subscriber_content_owner_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscriber',
            name='subscribed_to',
        ),
        migrations.AddField(
            model_name='subscriber',
            name='subscription',
            field=models.ManyToManyField(blank=True, related_name='subscriptions', to=settings.AUTH_USER_MODEL),
        ),
    ]