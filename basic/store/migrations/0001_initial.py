# Generated by Django 3.2.5 on 2021-08-24 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_details', models.SmallIntegerField()),
                ('quantity', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Stock_History',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('instock_qty', models.PositiveIntegerField()),
                ('after_process', models.IntegerField()),
                ('change_in_qty', models.IntegerField()),
                ('process', models.CharField(max_length=1024)),
            ],
        ),
    ]