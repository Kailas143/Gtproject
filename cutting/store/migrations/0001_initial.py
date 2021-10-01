# Generated by Django 3.2.7 on 2021-10-01 05:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tenant_id', models.PositiveIntegerField()),
                ('raw_materials', models.PositiveIntegerField()),
                ('quantity', models.FloatField()),
                ('financial_period', models.DateField(auto_now=True)),
                ('min_stock', models.FloatField()),
                ('max_stock', models.FloatField()),
                ('avg_stock', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Stock_History',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tenant_id', models.PositiveIntegerField()),
                ('instock_qty', models.FloatField()),
                ('after_process', models.FloatField(blank=True, null=True)),
                ('change_in_qty', models.FloatField(blank=True, null=True)),
                ('process', models.CharField(max_length=1024)),
                ('date_time', models.DateTimeField(auto_now=True)),
                ('financial_period', models.DateField(auto_now=True)),
                ('stock_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.stock')),
            ],
        ),
    ]
