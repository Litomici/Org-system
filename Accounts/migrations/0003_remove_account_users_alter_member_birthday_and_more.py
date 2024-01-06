# Generated by Django 4.2.7 on 2023-12-31 01:18

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Accounts', '0002_alter_member_birthday'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='users',
        ),
        migrations.AlterField(
            model_name='member',
            name='birthday',
            field=models.DateField(default=datetime.datetime(2023, 12, 31, 1, 18, 49, 483483, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AddField(
            model_name='account',
            name='users',
            field=models.ManyToManyField(default=[models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)], related_name='access_users', to=settings.AUTH_USER_MODEL),
        ),
    ]
