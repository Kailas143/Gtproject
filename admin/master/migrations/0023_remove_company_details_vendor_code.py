# Generated by Django 3.2.7 on 2021-11-21 10:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0022_alter_company_details_vendor_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company_details',
            name='vendor_code',
        ),
    ]
