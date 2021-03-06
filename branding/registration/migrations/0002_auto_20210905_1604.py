# Generated by Django 3.2.5 on 2021-09-05 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='register',
            name='slug',
        ),
        migrations.AlterField(
            model_name='register',
            name='company',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='register',
            name='first_name',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='register',
            name='last_name',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='register',
            name='middle_name',
            field=models.CharField(max_length=150),
        ),
    ]
