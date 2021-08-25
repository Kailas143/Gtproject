# Generated by Django 3.2.5 on 2021-08-24 09:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_alter_stock_product_details'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock_history',
            name='stock_table',
            field=models.ForeignKey(default=10, on_delete=django.db.models.deletion.CASCADE, to='store.stock'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='stock_history',
            name='instock_qty',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
