# Generated by Django 3.2.5 on 2021-09-05 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0002_auto_20210905_1604'),
    ]

    operations = [
        migrations.AlterField(
            model_name='register',
            name='middle_name',
            field=models.CharField(max_length=150, null=True),
        ),
    ]