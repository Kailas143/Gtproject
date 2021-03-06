# Generated by Django 3.2.7 on 2021-11-20 07:12

from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='main_process',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('process_name', models.CharField(max_length=1024)),
                ('test', models.CharField(max_length=1024, null=True)),
                ('cost', models.FloatField(null=True)),
                ('slug', models.SlugField(unique=True)),
                ('mixing', models.BooleanField(default=False)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='production_master.main_process')),
            ],
            options={
                'verbose_name_plural': 'mainprocess',
                'unique_together': {('parent', 'slug')},
            },
        ),
        migrations.CreateModel(
            name='sub_process',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('process_name', models.CharField(max_length=1054)),
                ('stage', models.PositiveIntegerField()),
                ('tenant_id', models.PositiveIntegerField()),
                ('financial_period', models.DateField(auto_now_add=True)),
                ('worker_name', models.CharField(max_length=1054)),
                ('mainprocess', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='production_master.main_process')),
            ],
        ),
        migrations.CreateModel(
            name='productioncard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tenant_id', models.PositiveIntegerField()),
                ('product_price', models.PositiveIntegerField()),
                ('accepted_qty', models.FloatField()),
                ('rework_qty', models.FloatField()),
                ('rejected_qty', models.FloatField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('financial_period', models.DateField(auto_now_add=True)),
                ('worker_name', models.CharField(max_length=1054)),
                ('sub_process', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='production_master.sub_process')),
            ],
        ),
    ]
