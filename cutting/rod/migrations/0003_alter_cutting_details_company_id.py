# Generated by Django 3.2.7 on 2021-10-01 04:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rod', '0002_auto_20211001_0932'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cutting_details',
            name='company_id',
            field=models.PositiveIntegerField(),
        ),
    ]
