# Generated by Django 4.2 on 2024-01-09 15:49

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('transaction', '0001_initial'),
        ('customer', '0003_alter_customer_user'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Customer',
            new_name='CustomerModel',
        ),
    ]
