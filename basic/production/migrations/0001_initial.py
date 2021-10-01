# Generated by Django 3.2.7 on 2021-09-27 04:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Mainprocess',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('process_name', models.CharField(max_length=1054)),
                ('stage', models.PositiveIntegerField()),
                ('tenant_id', models.PositiveIntegerField()),
                ('financial_period', models.DateField(auto_now_add=True)),
                ('worker_name', models.CharField(max_length=1054)),
            ],
        ),
        migrations.CreateModel(
            name='Subprocess',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('process_name', models.PositiveIntegerField()),
                ('stage', models.PositiveIntegerField()),
                ('tenant_id', models.PositiveIntegerField()),
                ('financial_period', models.DateField(auto_now_add=True)),
                ('worker_name', models.CharField(max_length=1054)),
                ('mainprocess', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='production.mainprocess')),
            ],
        ),
        migrations.CreateModel(
            name='Production',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tenant_id', models.PositiveIntegerField()),
                ('accepted_qty', models.FloatField()),
                ('rework_qty', models.FloatField()),
                ('rejected_qty', models.FloatField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('financial_period', models.DateField(auto_now_add=True)),
                ('worker_name', models.CharField(max_length=1054)),
                ('process', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='production.subprocess')),
            ],
        ),
    ]
