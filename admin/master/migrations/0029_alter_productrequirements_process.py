# Generated by Django 3.2.7 on 2021-12-03 06:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0028_alter_product_unit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productrequirements',
            name='process',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='master.process'),
        ),
    ]
