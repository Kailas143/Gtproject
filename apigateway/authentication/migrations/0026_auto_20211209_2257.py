# Generated by Django 3.2.7 on 2021-12-09 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0025_auto_20211209_1829'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tenant_company',
            name='address',
        ),
        migrations.RemoveField(
            model_name='tenant_company',
            name='city',
        ),
        migrations.RemoveField(
            model_name='tenant_company',
            name='country',
        ),
        migrations.RemoveField(
            model_name='tenant_company',
            name='state',
        ),
        migrations.AddField(
            model_name='tenant_company',
            name='address_line1',
            field=models.CharField(max_length=1024, null=True),
        ),
        migrations.AddField(
            model_name='tenant_company',
            name='address_line2',
            field=models.CharField(max_length=1024, null=True),
        ),
        migrations.AddField(
            model_name='tenant_company',
            name='address_line3',
            field=models.CharField(max_length=1024, null=True),
        ),
    ]
