# Generated by Django 3.2.7 on 2021-11-22 08:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0016_rename_menu_menu_section'),
    ]

    operations = [
        migrations.DeleteModel(
            name='menu_section',
        ),
    ]
