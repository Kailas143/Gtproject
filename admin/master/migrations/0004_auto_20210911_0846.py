# Generated by Django 3.2.5 on 2021-09-11 08:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0003_alter_product_tenant_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='company_details',
            name='worker_name',
            field=models.CharField(default='Vinu', max_length=1024),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='process',
            name='worker_name',
            field=models.CharField(default='Vinu', max_length=1024),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='processcost',
            name='worker_name',
            field=models.CharField(default='Vinu', max_length=1024),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='worker_name',
            field=models.CharField(default='Vinu', max_length=1024),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='productrequirements',
            name='product',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='master.product'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='productrequirements',
            name='worker_name',
            field=models.CharField(default='Vinu', max_length=1024),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='productspec',
            name='worker_name',
            field=models.CharField(default='Vinu', max_length=1024),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='rawcomponent',
            name='worker_name',
            field=models.CharField(default='Vinu', max_length=1024),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='supliers_contact_details',
            name='worker_name',
            field=models.CharField(default='Vinu', max_length=1024),
            preserve_default=False,
        ),
    ]
