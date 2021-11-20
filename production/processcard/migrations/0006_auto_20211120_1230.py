# Generated by Django 3.2.7 on 2021-11-20 07:00

from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('processcard', '0005_auto_20211120_1000'),
    ]

    operations = [
        # migrations.CreateModel(
        #     name='Mainprocess_details',
        #     fields=[
        #         ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
        #         ('process_name', models.CharField(max_length=1024)),
        #         ('test', models.CharField(max_length=1024, null=True)),
        #         ('cost', models.FloatField(null=True)),
        #         ('slug', models.SlugField(unique=True)),
        #         ('mixing', models.BooleanField(default=False)),
        #         ('lft', models.PositiveIntegerField(editable=False)),
        #         ('rght', models.PositiveIntegerField(editable=False)),
        #         ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
        #         ('level', models.PositiveIntegerField(editable=False)),
        #         ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='processcard.mainprocess_details')),
        #     ],
        #     options={
        #         'verbose_name_plural': 'mainprocess',
        #         'unique_together': {('parent', 'slug')},
        #     },
        # ),
        migrations.RemoveField(
            model_name='mainprocess',
            name='process_details',
        ),
        migrations.DeleteModel(
            name='process_name',
        ),
        migrations.AlterField(
            model_name='subprocess',
            name='mainprocess',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='processcard.mainprocess_details'),
        ),
        migrations.DeleteModel(
            name='Mainprocess',
        ),
    ]
