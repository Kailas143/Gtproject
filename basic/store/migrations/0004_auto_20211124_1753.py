# Generated by Django 3.2.7 on 2021-11-24 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_stock_history_tenant_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='avg_stock',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='max_stock',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='min_stock',
            field=models.FloatField(null=True),
        ),
    ]
