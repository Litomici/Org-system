# Generated by Django 4.2.7 on 2024-01-27 20:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0005_alter_member_birthday'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='birthday',
            field=models.DateField(default=datetime.datetime(2024, 1, 27, 20, 14, 28, 174037, tzinfo=datetime.timezone.utc)),
        ),
    ]