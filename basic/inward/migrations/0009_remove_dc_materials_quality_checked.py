# Generated by Django 3.2.7 on 2021-11-10 11:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inward', '0008_dc_materials_quality_checked'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dc_materials',
            name='quality_checked',
        ),
    ]
