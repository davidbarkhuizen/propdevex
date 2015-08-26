# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BinaryUpload',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('source_path', models.CharField(max_length=1024, blank=True)),
                ('destination_path', models.CharField(max_length=1024, blank=True)),
            ],
            options={
                'db_table': 'binaryupload',
            },
        ),
        migrations.CreateModel(
            name='FRP_Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=1024)),
            ],
            options={
                'db_table': 'frp_category',
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.CreateModel(
            name='FRP_Contact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=1024)),
                ('phone', models.CharField(max_length=1024)),
                ('email', models.CharField(max_length=1024)),
                ('isprimary', models.BooleanField(default=False)),
                ('iscc', models.BooleanField(default=False)),
                ('categories', models.ManyToManyField(to='server.FRP_Category', blank=True)),
            ],
            options={
                'db_table': 'frp_contact',
                'verbose_name': 'contact',
                'verbose_name_plural': 'contacts',
            },
        ),
        migrations.CreateModel(
            name='FRP_Property',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sold', models.BooleanField(default=False)),
                ('name', models.CharField(unique=True, max_length=1024)),
                ('areaSQM', models.IntegerField(null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('shortLocation', models.CharField(max_length=1024)),
                ('longLocation', models.CharField(max_length=1024)),
                ('latitude', models.DecimalField(null=True, max_digits=9, decimal_places=6, blank=True)),
                ('longitude', models.DecimalField(null=True, max_digits=9, decimal_places=6, blank=True)),
                ('category', models.ForeignKey(to='server.FRP_Category')),
            ],
            options={
                'db_table': 'frp_property',
                'verbose_name': 'property',
                'verbose_name_plural': 'properties',
            },
        ),
        migrations.CreateModel(
            name='FRP_PropertyImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file', models.FileField(upload_to=b'frp/image')),
                ('isprimary', models.BooleanField(default=False)),
                ('property', models.ForeignKey(to='server.FRP_Property')),
            ],
            options={
                'db_table': 'frp_property_image',
                'verbose_name': 'propertyimage',
                'verbose_name_plural': 'propertyimages',
            },
        ),
        migrations.CreateModel(
            name='FRP_SubProperty',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sold', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=1024, null=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('areaSQM', models.IntegerField(null=True, blank=True)),
                ('property', models.ForeignKey(to='server.FRP_Property')),
            ],
            options={
                'db_table': 'frp_sub_property',
                'verbose_name': 'subproperty',
                'verbose_name_plural': 'subproperties',
            },
        ),
        migrations.CreateModel(
            name='FRP_SubPropertyImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file', models.FileField(upload_to=b'frp/image')),
                ('isprimary', models.BooleanField(default=False)),
                ('subproperty', models.ForeignKey(to='server.FRP_SubProperty')),
            ],
            options={
                'db_table': 'frp_sub_property_image',
                'verbose_name': 'subpropertyimage',
                'verbose_name_plural': 'subpropertyimages',
            },
        ),
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=1024, blank=True)),
                ('token', models.CharField(unique=True, max_length=1024, blank=True)),
                ('json_data_model', models.TextField(null=True, blank=True)),
                ('update', models.BooleanField(default=False)),
                ('last_updated_at', models.DateTimeField(null=True, blank=True)),
                ('update_log_message', models.CharField(max_length=1024, null=True, blank=True)),
                ('ftp_host', models.CharField(max_length=1024, blank=True)),
                ('ftp_port', models.IntegerField()),
                ('ftp_user', models.CharField(max_length=1024, blank=True)),
                ('ftp_password', models.CharField(max_length=1024, blank=True)),
                ('ftp_account', models.CharField(max_length=1024, null=True, blank=True)),
                ('ftp_upload_root', models.CharField(max_length=1024, null=True, blank=True)),
                ('users', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'site',
            },
        ),
        migrations.CreateModel(
            name='TextUpload',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('source_path', models.CharField(max_length=1024, blank=True)),
                ('destination_path', models.CharField(max_length=1024, blank=True)),
                ('site', models.ForeignKey(to='server.Site')),
            ],
            options={
                'db_table': 'textupload',
            },
        ),
        migrations.AddField(
            model_name='binaryupload',
            name='site',
            field=models.ForeignKey(to='server.Site'),
        ),
    ]
