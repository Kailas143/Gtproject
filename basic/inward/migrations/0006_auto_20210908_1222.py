# Generated by Django 3.2.5 on 2021-09-08 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inward', '0005_auto_20210908_1201'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dc_materials',
            name='item',
        ),
        migrations.AddField(
            model_name='dc_materials',
            name='raw_materials',
            field=models.PositiveIntegerField(default='1'),
            preserve_default=False,
        ),
    ]