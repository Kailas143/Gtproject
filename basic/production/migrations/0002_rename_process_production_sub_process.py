# Generated by Django 3.2.7 on 2021-09-27 08:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='production',
            old_name='process',
            new_name='sub_process',
        ),
    ]
