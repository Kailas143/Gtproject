# Generated by Django 3.2.7 on 2021-12-09 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0024_auto_20211122_1532'),
    ]

    operations = [
        migrations.AddField(
            model_name='tenant_company',
            name='acc_no',
            field=models.CharField(blank=True, max_length=1024, null=True),
        ),
        migrations.AddField(
            model_name='tenant_company',
            name='bank_name',
            field=models.CharField(blank=True, max_length=1024, null=True),
        ),
        migrations.AddField(
            model_name='tenant_company',
            name='branch_name',
            field=models.CharField(blank=True, max_length=1024, null=True),
        ),
        migrations.AddField(
            model_name='tenant_company',
            name='gst_no',
            field=models.CharField(blank=True, max_length=1024, null=True),
        ),
        migrations.AddField(
            model_name='tenant_company',
            name='ifsc_code',
            field=models.CharField(blank=True, max_length=1024, null=True),
        ),
        migrations.AddField(
            model_name='tenant_company',
            name='office_email',
            field=models.CharField(blank=True, max_length=1024, null=True),
        ),
        migrations.AddField(
            model_name='tenant_company',
            name='office_pnone_no',
            field=models.CharField(blank=True, max_length=1024, null=True),
        ),
    ]