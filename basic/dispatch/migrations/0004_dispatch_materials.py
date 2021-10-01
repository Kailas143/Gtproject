# Generated by Django 3.2.5 on 2021-09-15 05:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dispatch', '0003_dispatch_details_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dispatch_materials',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tenant_id', models.PositiveIntegerField()),
                ('product_details', models.PositiveIntegerField()),
                ('qty', models.FloatField()),
                ('bal_qty', models.FloatField()),
                ('error_qty', models.FloatField()),
                ('financial_period', models.DateField(auto_now=True)),
                ('dispatch_details', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dispatch.dispatch_details')),
            ],
        ),
    ]
