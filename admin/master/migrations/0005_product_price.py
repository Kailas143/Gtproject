# Generated by Django 3.2.7 on 2021-09-28 04:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0004_auto_20210911_0846'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product_price',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField()),
                ('expiry_price', models.FloatField(null=True)),
                ('expiry_status', models.BooleanField(default=False)),
                ('financial_period', models.DateField(auto_now=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='master.company_details')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='master.product')),
            ],
        ),
    ]
