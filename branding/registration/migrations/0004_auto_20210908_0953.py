# Generated by Django 3.2.5 on 2021-09-08 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0003_alter_register_middle_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='register',
            name='company',
        ),
        migrations.AddField(
            model_name='register',
            name='address',
            field=models.TextField(default='Kollam', max_length=1024),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='register',
            name='city',
            field=models.CharField(default='Coimbatore', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='register',
            name='company_name',
            field=models.CharField(default='sks', max_length=1024),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='register',
            name='country',
            field=models.CharField(default='India', max_length=1024),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='register',
            name='phone_number',
            field=models.CharField(default='1234567890', max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='register',
            name='state',
            field=models.CharField(default='Kerala', max_length=1024),
            preserve_default=False,
        ),
    ]