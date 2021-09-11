# Generated by Django 3.2.5 on 2021-09-07 09:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='company_details',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(blank=True, max_length=1024, null=True)),
                ('address_line1', models.CharField(max_length=1024, null=True)),
                ('address_line2', models.CharField(max_length=1024, null=True)),
                ('address_line3', models.CharField(max_length=1024, null=True)),
                ('office_email', models.CharField(blank=True, max_length=1024, null=True)),
                ('office_pnone_no', models.CharField(blank=True, max_length=1024, null=True)),
                ('gst_no', models.CharField(blank=True, max_length=1024, null=True)),
                ('acc_no', models.CharField(blank=True, max_length=1024, null=True)),
                ('ifsc_code', models.CharField(blank=True, max_length=1024, null=True)),
                ('bank_name', models.CharField(blank=True, max_length=1024, null=True)),
                ('branch_name', models.CharField(blank=True, max_length=1024, null=True)),
                ('purchase_company', models.BooleanField(default=True)),
                ('ratings', models.IntegerField(null=True)),
                ('vendor_code', models.CharField(blank=True, max_length=1024, null=True)),
                ('description', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Process',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('process_name', models.CharField(max_length=1024)),
                ('test', models.CharField(max_length=1024)),
                ('cost', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Productspec',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('spec', models.CharField(max_length=1024)),
                ('value', models.FloatField()),
                ('unit', models.CharField(max_length=1024)),
            ],
        ),
        migrations.CreateModel(
            name='Rawcomponent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rname', models.CharField(max_length=1024)),
                ('code', models.CharField(max_length=200, unique=True)),
                ('grade', models.CharField(max_length=1024)),
                ('main_component', models.BooleanField(default=True)),
                ('material', models.CharField(max_length=1024)),
            ],
        ),
        migrations.CreateModel(
            name='Roles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('roles', models.CharField(max_length=1024)),
            ],
        ),
        migrations.CreateModel(
            name='supliers_contact_details',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=1024, null=True)),
                ('phone_no', models.CharField(max_length=1024, null=True)),
                ('name', models.CharField(max_length=1024, null=True)),
                ('post', models.CharField(max_length=1024, null=True)),
                ('company_details', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='master.company_details')),
            ],
        ),
        migrations.CreateModel(
            name='Productrequirements',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.FloatField()),
                ('process', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='master.process')),
                ('raw_component', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='master.rawcomponent')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pname', models.CharField(max_length=1024, verbose_name='Product Name')),
                ('billed_name', models.CharField(max_length=1024, verbose_name='Billed Name')),
                ('cost', models.FloatField(blank=True)),
                ('IGST', models.FloatField(blank=True)),
                ('SGST', models.FloatField()),
                ('CGST', models.FloatField()),
                ('code', models.CharField(max_length=200, unique=True)),
                ('job_name', models.CharField(max_length=1024)),
                ('main_component', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='master.rawcomponent')),
            ],
        ),
        migrations.CreateModel(
            name='Processcost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cycle_time', models.TimeField()),
                ('type_of_tools', models.CharField(choices=[('t', 'Tools'), ('i', 'Instrunmental')], default='Tools', max_length=1024)),
                ('process_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='master.process')),
            ],
        ),
    ]
