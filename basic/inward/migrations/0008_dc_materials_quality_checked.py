# Generated by Django 3.2.7 on 2021-11-10 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inward', '0007_alter_dc_details_tenant_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='dc_materials',
            name='quality_checked',
            field=models.BooleanField(default=False),
        ),
    ]