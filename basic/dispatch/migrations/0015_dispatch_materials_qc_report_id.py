# Generated by Django 3.2.7 on 2021-12-11 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dispatch', '0014_alter_dispatch_materials_dispatch_details'),
    ]

    operations = [
        migrations.AddField(
            model_name='dispatch_materials',
            name='qc_report_id',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
    ]