# Generated by Django 3.2.5 on 2021-09-01 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_auto_20210824_0930'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock_history',
            name='date_time',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='stock_history',
            name='after_process',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='stock_history',
            name='change_in_qty',
            field=models.FloatField(blank=True, null=True),
        ),
    ]