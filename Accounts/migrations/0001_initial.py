# Generated by Django 4.2.7 on 2023-12-31 01:02

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailConfirmation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('token', models.CharField(max_length=128, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jmeno', models.CharField(default='john', max_length=30)),
                ('surname', models.CharField(default='Smith', max_length=40)),
                ('birthday', models.DateField(default=datetime.datetime(2023, 12, 31, 1, 2, 12, 755421, tzinfo=datetime.timezone.utc))),
                ('ATOM_id', models.CharField(blank=True, max_length=18)),
                ('GDPR', models.BooleanField(default=True)),
                ('healthProblems', models.CharField(default='Dítě nemá žádná zdravotní omezení ani speciální požadavky na stravu či zacházení')),
            ],
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('addres1', models.CharField(default='')),
                ('city1', models.CharField(default='')),
                ('psc1', models.CharField(default='')),
                ('mobile1', models.CharField(default='', max_length=13)),
                ('addres2', models.CharField(blank=True, default='')),
                ('city2', models.CharField(blank=True, default='')),
                ('psc2', models.CharField(blank=True, default='')),
                ('mobile2', models.CharField(default='', max_length=13)),
                ('wallet', models.FloatField(default=0.0)),
                ('position', models.IntegerField(default=0)),
                ('member', models.ManyToManyField(blank=True, related_name='members', to='Accounts.member')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('users', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='access_users', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
