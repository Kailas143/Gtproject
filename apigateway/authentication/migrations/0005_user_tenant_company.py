# Generated by Django 3.2.5 on 2021-09-08 10:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_auto_20210908_1052'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='tenant_company',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, related_name='tenant_company', to='authentication.tenant_company'),
            preserve_default=False,
        ),
    ]
