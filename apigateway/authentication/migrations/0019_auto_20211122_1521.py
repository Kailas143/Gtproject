# Generated by Django 3.2.7 on 2021-11-22 09:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0018_menu_tab'),
    ]

    operations = [
        migrations.CreateModel(
            name='menu_link',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.CharField(max_length=1024)),
                ('name', models.CharField(max_length=1024)),
                ('service', models.CharField(max_length=1024)),
            ],
        ),
        migrations.RemoveField(
            model_name='menu_tab',
            name='mixing',
        ),
        # migrations.AddField(
        #     model_name='menu_tab',
        #     name='menu_link',
        #     field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='menu_link', to='authentication.menu_link'),
        #     preserve_default=False,
        # ),
    ]
