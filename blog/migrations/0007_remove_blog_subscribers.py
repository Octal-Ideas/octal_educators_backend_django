# Generated by Django 4.2 on 2023-06-05 09:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_blog_subscribers_alter_blog_thumbnail'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blog',
            name='subscribers',
        ),
    ]