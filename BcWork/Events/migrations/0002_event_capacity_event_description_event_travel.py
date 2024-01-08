# Generated by Django 4.2.7 on 2024-01-03 00:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Events', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='capacity',
            field=models.IntegerField(blank=True, default=50),
        ),
        migrations.AddField(
            model_name='event',
            name='description',
            field=models.CharField(blank=True, default=' '),
        ),
        migrations.AddField(
            model_name='event',
            name='travel',
            field=models.BooleanField(blank=True, default=True),
        ),
    ]