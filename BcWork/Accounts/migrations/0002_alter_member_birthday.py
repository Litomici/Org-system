# Generated by Django 4.2.7 on 2023-12-31 01:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='birthday',
            field=models.DateField(default=datetime.datetime(2023, 12, 31, 1, 2, 26, 235728, tzinfo=datetime.timezone.utc)),
        ),
    ]