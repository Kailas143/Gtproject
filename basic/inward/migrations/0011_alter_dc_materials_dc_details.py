# Generated by Django 3.2.7 on 2021-12-01 06:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inward', '0010_alter_dc_details_dc_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dc_materials',
            name='dc_details',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='materials', to='inward.dc_details'),
        ),
    ]
