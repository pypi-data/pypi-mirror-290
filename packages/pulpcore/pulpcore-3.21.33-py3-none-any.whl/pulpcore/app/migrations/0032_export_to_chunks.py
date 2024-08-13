# Generated by Django 2.2.11 on 2020-05-22 18:31

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0031_import_export_validate_params'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pulpexport',
            name='filename',
        ),
        migrations.RemoveField(
            model_name='pulpexport',
            name='sha256',
        ),
        migrations.AddField(
            model_name='pulpexport',
            name='output_file_info',
            field=django.contrib.postgres.fields.jsonb.JSONField(null=True),
        ),
    ]
