# Generated by Django 3.2.5 on 2021-09-02 04:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_alter_stock_history_managers'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='stock_history',
            managers=[
            ],
        ),
        migrations.AddField(
            model_name='stock',
            name='financial_period',
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name='stock_history',
            name='financial_period',
            field=models.DateField(auto_now=True),
        ),
    ]
