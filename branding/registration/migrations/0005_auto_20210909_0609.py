# Generated by Django 3.2.5 on 2021-09-09 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0004_auto_20210908_0953'),
    ]

    operations = [
        migrations.AlterField(
            model_name='register',
            name='first_name',
            field=models.CharField(max_length=1024),
        ),
        migrations.AlterField(
            model_name='register',
            name='last_name',
            field=models.CharField(max_length=1024),
        ),
        migrations.AlterField(
            model_name='register',
            name='middle_name',
            field=models.CharField(max_length=1024, null=True),
        ),
    ]