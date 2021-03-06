# Generated by Django 3.2.5 on 2021-09-15 15:52

import django.contrib.auth.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tenant_Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=1024)),
                ('address', models.TextField()),
                ('phone_number', models.CharField(max_length=10)),
                ('city', models.CharField(max_length=1024)),
                ('state', models.CharField(max_length=1024)),
                ('country', models.CharField(max_length=1024)),
                ('joined_data', models.DateField(auto_now=True)),
                ('domain', models.CharField(max_length=1024)),
            ],
        ),
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.RemoveField(
            model_name='user',
            name='domain',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_admin',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_employee',
        ),
    ]
