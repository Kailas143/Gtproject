# Generated by Django 3.2.5 on 2021-09-01 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dispatch', '0003_rename_inward_date_dispatch_details_dispatch_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dispatch_details',
            name='dispatch_worker',
            field=models.CharField(max_length=1024, null=True),
        ),
    ]
