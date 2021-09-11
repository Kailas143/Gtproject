# Generated by Django 3.2.5 on 2021-09-08 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inward', '0004_dc_materials_financial_period'),
    ]

    operations = [
        migrations.AddField(
            model_name='dc_details',
            name='tenant_id',
            field=models.PositiveIntegerField(default='1'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dc_materials',
            name='tenant_id',
            field=models.PositiveIntegerField(default='1'),
            preserve_default=False,
        ),
    ]