# Generated by Django 3.0.5 on 2020-05-24 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account_settings', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='aboutme',
            name='activate',
            field=models.BooleanField(default=False, verbose_name='Activate in search?'),
        ),
    ]
