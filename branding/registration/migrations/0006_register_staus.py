# Generated by Django 3.2.5 on 2021-09-10 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0005_auto_20210909_0609'),
    ]

    operations = [
        migrations.AddField(
            model_name='register',
            name='staus',
            field=models.CharField(choices=[('Accepted', 'Accepted'), ('Pending', 'Pending'), ('Rejected', 'Rejected')], default='Rejected', max_length=50),
        ),
    ]