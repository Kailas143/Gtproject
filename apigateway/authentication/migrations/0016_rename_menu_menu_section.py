# Generated by Django 3.2.7 on 2021-11-22 08:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0015_menu'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='menu',
            new_name='menu_section',
        ),
    ]
