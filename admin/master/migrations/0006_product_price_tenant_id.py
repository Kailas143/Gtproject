# Generated by Django 3.2.7 on 2021-09-28 05:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0005_product_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='product_price',
            name='tenant_id',
            field=models.PositiveIntegerField(),
            preserve_default=False,
        ),
    ]
