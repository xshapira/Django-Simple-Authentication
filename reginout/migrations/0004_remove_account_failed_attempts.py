# Generated by Django 3.2.6 on 2021-08-24 14:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reginout', '0003_account_failed_attempts'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='failed_attempts',
        ),
    ]
