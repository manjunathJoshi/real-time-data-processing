# Generated by Django 3.1.2 on 2022-04-11 18:13

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DataTransformer', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='datastreampacket',
            old_name='payload',
            new_name='raw_payload',
        ),
        migrations.AddField(
            model_name='datastreampacket',
            name='transformed_data',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), blank=True, null=True, size=None),
        ),
        migrations.AlterUniqueTogether(
            name='datastreampacket',
            unique_together={('data_packet_index', 'primary_resource_id')},
        ),
        migrations.DeleteModel(
            name='AncillaryProcessor',
        ),
    ]