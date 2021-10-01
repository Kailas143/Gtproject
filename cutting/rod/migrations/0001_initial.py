# Generated by Django 3.2.7 on 2021-09-30 09:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='cutting_details',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tenant_id', models.PositiveIntegerField()),
                ('company_id', models.SmallIntegerField()),
                ('cutting_number', models.PositiveIntegerField(unique=True)),
                ('cutting_date', models.DateTimeField(auto_now=True)),
                ('cutting_worker', models.CharField(max_length=1024, null=True)),
                ('financial_period', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='semi_product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tenant_id', models.CharField(max_length=1024)),
                ('sp_name', models.CharField(max_length=1024)),
                ('billed_name', models.CharField(max_length=1024)),
                ('cost', models.FloatField()),
                ('IGST', models.FloatField()),
                ('SGST', models.FloatField()),
                ('CGST', models.FloatField()),
                ('code', models.CharField(max_length=200, unique=True)),
                ('job_name', models.CharField(max_length=1024)),
                ('raw_material', models.PositiveIntegerField()),
                ('worker_name', models.CharField(max_length=1024)),
                ('financial_period', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='semi_product_price',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tenant_id', models.PositiveIntegerField()),
                ('company', models.PositiveIntegerField()),
                ('price', models.FloatField()),
                ('expiry_price', models.FloatField(null=True)),
                ('expiry_status', models.BooleanField(default=False)),
                ('financial_period', models.DateField(auto_now=True)),
                ('semi_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rod.semi_product')),
            ],
        ),
        migrations.CreateModel(
            name='cutting_materials',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tenant_id', models.PositiveIntegerField()),
                ('qty', models.FloatField()),
                ('bal_qty', models.FloatField()),
                ('error_qty', models.FloatField()),
                ('financial_period', models.DateField(auto_now=True)),
                ('cutting_details_details', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rod.cutting_details')),
                ('semi_product_details', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rod.semi_product_price')),
            ],
        ),
    ]
