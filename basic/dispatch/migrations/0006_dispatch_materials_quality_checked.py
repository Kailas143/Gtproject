# Generated by Django 3.2.7 on 2021-11-10 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dispatch', '0005_remove_dispatch_details_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='dispatch_materials',
            name='quality_checked',
            field=models.BooleanField(default=False),
        ),
    ]