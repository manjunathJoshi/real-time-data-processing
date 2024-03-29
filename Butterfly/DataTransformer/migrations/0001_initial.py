# Generated by Django 3.1.2 on 2022-04-10 14:36

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DataStream',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('primary_resource_id', models.IntegerField(db_index=True)),
                ('stream_transferd', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DataStreamPacket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('data_packet_index', models.IntegerField(db_index=True)),
                ('payload', models.BinaryField(default=b'default text')),
                ('primary_resource_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DataTransformer.datastream')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AncillaryProcessor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('transformed_data', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), size=None)),
                ('data_packet_index', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DataTransformer.datastreampacket')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
