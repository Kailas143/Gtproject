# Generated by Django 3.2.5 on 2021-09-15 05:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dispatch', '0004_dispatch_materials'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dispatch_details',
            name='name',
        ),
    ]
