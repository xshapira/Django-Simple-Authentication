# Generated by Django 3.2.6 on 2021-08-24 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reginout', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
    ]
