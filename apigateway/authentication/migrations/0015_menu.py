# Generated by Django 3.2.7 on 2021-11-22 08:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0014_service'),
    ]

    operations = [
        migrations.CreateModel(
            name='menu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1024)),
                ('slug', models.SlugField(unique=True)),
                ('mixing', models.BooleanField(default=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='authentication.menu')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'mainprocess',
                'unique_together': {('parent', 'slug')},
            },
        ),
    ]