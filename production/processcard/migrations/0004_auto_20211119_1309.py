# Generated by Django 3.2.7 on 2021-11-19 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('processcard', '0003_auto_20211012_1254'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subprocess',
            name='product_price',
        ),
        migrations.AddField(
            model_name='production_card',
            name='product_price',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
    ]
