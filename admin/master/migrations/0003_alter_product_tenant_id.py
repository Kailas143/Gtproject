# Generated by Django 3.2.5 on 2021-09-10 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0002_auto_20210908_1206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='tenant_id',
            field=models.CharField(max_length=1024),
        ),
    ]
