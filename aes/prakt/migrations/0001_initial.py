# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AcademicDegree',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('degree', models.CharField(max_length=50, verbose_name=b'\xd0\x9d\xd0\xb0\xd0\xb8\xd0\xbc\xd0\xb5\xd0\xbd\xd0\xbe\xd0\xb2\xd0\xb0\xd0\xbd\xd0\xb8\xd0\xb5')),
                ('degree_short', models.CharField(max_length=10, verbose_name=b'\xd0\xa1\xd0\xbe\xd0\xba\xd1\x80\xd0\xb0\xd1\x89\xd1\x91\xd0\xbd\xd0\xbd\xd0\xbe')),
            ],
        ),
        migrations.CreateModel(
            name='AcademicStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.CharField(max_length=50, verbose_name=b'\xd0\x9d\xd0\xb0\xd0\xb8\xd0\xbc\xd0\xb5\xd0\xbd\xd0\xbe\xd0\xb2\xd0\xb0\xd0\xbd\xd0\xb8\xd0\xb5')),
            ],
        ),
        migrations.CreateModel(
            name='Docs',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.CharField(max_length=100, verbose_name=b'\xd0\x9d\xd0\xbe\xd0\xbc\xd0\xb5\xd1\x80 \xd0\xb4\xd0\xbe\xd0\xba\xd1\x83\xd0\xbc\xd0\xb5\xd0\xbd\xd1\x82\xd0\xb0', blank=True)),
                ('date', models.DateField(null=True, verbose_name=b'\xd0\x94\xd0\xb0\xd1\x82\xd0\xb0 \xd0\xb4\xd0\xbe\xd0\xba\xd1\x83\xd0\xbc\xd0\xb5\xd0\xbd\xd1\x82\xd0\xb0', blank=True)),
                ('description', models.CharField(max_length=150, verbose_name=b'\xd0\x9e\xd0\xbf\xd0\xb8\xd1\x81\xd0\xb0\xd0\xbd\xd0\xb8\xd0\xb5', blank=True)),
                ('file', models.FileField(upload_to=b'', verbose_name=b'\xd0\xa4\xd0\xb0\xd0\xb9\xd0\xbb')),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fname', models.CharField(max_length=100, verbose_name=b'\xd0\x98\xd0\xbc\xd1\x8f')),
                ('sname', models.CharField(max_length=100, verbose_name=b'\xd0\x9e\xd1\x82\xd1\x87\xd0\xb5\xd1\x81\xd1\x82\xd0\xb2\xd0\xbe', blank=True)),
                ('lname', models.CharField(max_length=100, verbose_name=b'\xd0\xa4\xd0\xb0\xd0\xbc\xd0\xb8\xd0\xbb\xd0\xb8\xd1\x8f', blank=True)),
                ('phone', models.CharField(max_length=100, verbose_name=b'\xd0\xa2\xd0\xb5\xd0\xbb\xd0\xb5\xd1\x84\xd0\xbe\xd0\xbd', blank=True)),
                ('email', models.EmailField(max_length=100, verbose_name=b'\xd0\x9f\xd0\xbe\xd1\x87\xd1\x82\xd0\xb0', blank=True)),
                ('post', models.CharField(max_length=150, verbose_name=b'\xd0\x94\xd0\xbe\xd0\xbb\xd0\xb6\xd0\xbd\xd0\xbe\xd1\x81\xd1\x82\xd1\x8c', blank=True)),
                ('prakt', models.BooleanField(default=False, verbose_name=b'\xd0\x9f\xd1\x80\xd0\xb0\xd0\xba\xd1\x82\xd0\xb8\xd0\xba\xd0\xb0?')),
                ('comment', models.CharField(max_length=255, verbose_name=b'\xd0\x9f\xd1\x80\xd0\xb8\xd0\xbc\xd0\xb5\xd1\x87\xd0\xb0\xd0\xbd\xd0\xb8\xd1\x8f', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Events',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(null=True, verbose_name=b'\xd0\x94\xd0\xb0\xd1\x82\xd0\xb0')),
                ('description', models.TextField(max_length=500, null=True, verbose_name=b'\xd0\x9e\xd0\xbf\xd0\xb8\xd1\x81\xd0\xb0\xd0\xbd\xd0\xb8\xd0\xb5 \xd1\x81\xd0\xbe\xd0\xb1\xd1\x8b\xd1\x82\xd0\xb8\xd1\x8f')),
            ],
            options={
                'ordering': ('-date',),
            },
        ),
        migrations.CreateModel(
            name='EventType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=50, null=True, verbose_name=b'\xd0\xa2\xd0\xb8\xd0\xbf \xd1\x81\xd0\xbe\xd0\xb1\xd1\x8b\xd1\x82\xd0\xb8\xd1\x8f')),
                ('css', models.CharField(max_length=50, verbose_name=b'CSS \xd0\xba\xd0\xbb\xd0\xb0\xd1\x81\xd1\x81')),
            ],
        ),
        migrations.CreateModel(
            name='Org',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=150, verbose_name=b'\xd0\x9d\xd0\xb0\xd0\xb7\xd0\xb2\xd0\xb0\xd0\xbd\xd0\xb8\xd0\xb5 \xd0\xb4\xd0\xbb\xd1\x8f \xd0\xb1\xd0\xb0\xd0\xb7\xd1\x8b')),
                ('titleFull', models.CharField(max_length=255, verbose_name=b'\xd0\x9f\xd0\xbe\xd0\xbb\xd0\xbd\xd0\xbe\xd0\xb5 \xd0\xbd\xd0\xb0\xd0\xb8\xd0\xbc\xd0\xb5\xd0\xbd\xd0\xbe\xd0\xb2\xd0\xb0\xd0\xbd\xd0\xb8\xd0\xb5')),
                ('titleShort', models.CharField(max_length=200, verbose_name=b'\xd0\xa1\xd0\xbe\xd0\xba\xd1\x80\xd0\xb0\xd1\x89\xd0\xb5\xd0\xbd\xd0\xbd\xd0\xbe\xd0\xb5 \xd0\xbd\xd0\xb0\xd0\xb8\xd0\xbc\xd0\xb5\xd0\xbd\xd0\xbe\xd0\xb2\xd0\xb0\xd0\xbd\xd0\xb8\xd0\xb5')),
                ('address', models.CharField(max_length=255, verbose_name=b'\xd0\x90\xd0\xb4\xd1\x80\xd0\xb5\xd1\x81')),
                ('site', models.URLField(verbose_name=b'\xd0\xa1\xd0\xb0\xd0\xb9\xd1\x82', blank=True)),
                ('phone', models.CharField(max_length=200, verbose_name=b'\xd0\xa2\xd0\xb5\xd0\xbb\xd0\xb5\xd1\x84\xd0\xbe\xd0\xbd\xd1\x8b', blank=True)),
                ('terms', models.TextField(verbose_name=b'\xd0\xa3\xd1\x81\xd0\xbb\xd0\xbe\xd0\xb2\xd0\xb8\xd1\x8f \xd0\xbf\xd1\x80\xd0\xb0\xd0\xba\xd1\x82\xd0\xb8\xd0\xba\xd0\xb8', blank=True)),
            ],
            options={
                'ordering': ('title',),
            },
        ),
        migrations.CreateModel(
            name='Posts',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('post_name', models.CharField(max_length=30, verbose_name=b'\xd0\x9d\xd0\xb0\xd0\xb8\xd0\xbc\xd0\xb5\xd0\xbd\xd0\xbe\xd0\xb2\xd0\xb0\xd0\xbd\xd0\xb8\xd0\xb5')),
            ],
        ),
        migrations.CreateModel(
            name='Students',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fname', models.CharField(max_length=20, verbose_name=b'\xd0\x98\xd0\xbc\xd1\x8f')),
                ('sname', models.CharField(max_length=20, verbose_name=b'\xd0\x9e\xd1\x82\xd1\x87\xd0\xb5\xd1\x81\xd1\x82\xd0\xb2\xd0\xbe')),
                ('lname', models.CharField(max_length=20, verbose_name=b'\xd0\xa4\xd0\xb0\xd0\xbc\xd0\xb8\xd0\xbb\xd0\xb8\xd1\x8f')),
                ('group', models.CharField(max_length=4, verbose_name=b'\xd0\x93\xd1\x80\xd1\x83\xd0\xbf\xd0\xbf\xd0\xb0')),
                ('link', models.URLField(verbose_name=b'\xd0\xa1\xd1\x81\xd1\x8b\xd0\xbb\xd0\xba\xd0\xb0')),
            ],
            options={
                'ordering': ('lname',),
            },
        ),
        migrations.CreateModel(
            name='Tasks',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('deadline', models.DateField(verbose_name=b'\xd0\xa1\xd1\x80\xd0\xbe\xd0\xba \xd0\xb8\xd1\x81\xd0\xbf\xd0\xbe\xd0\xbb\xd0\xbd\xd0\xb5\xd0\xbd\xd0\xb8\xd1\x8f')),
                ('statuschangedate', models.DateField(null=True, verbose_name=b'\xd0\x94\xd0\xb0\xd1\x82\xd0\xb0 \xd0\xb8\xd0\xb7\xd0\xbc\xd0\xb5\xd0\xbd\xd0\xb5\xd0\xbd\xd0\xb8\xd1\x8f \xd1\x81\xd1\x82\xd0\xb0\xd1\x82\xd1\x83\xd1\x81\xd0\xb0')),
                ('description', models.TextField(max_length=500, verbose_name=b'\xd0\x9e\xd0\xbf\xd0\xb8\xd1\x81\xd0\xb0\xd0\xbd\xd0\xb8\xd0\xb5')),
                ('org', models.ForeignKey(verbose_name=b'\xd0\x9e\xd1\x80\xd0\xb3\xd0\xb0\xd0\xbd\xd0\xb8\xd0\xb7\xd0\xb0\xd1\x86\xd0\xb8\xd1\x8f', blank=True, to='prakt.Org')),
            ],
            options={
                'ordering': ('deadline',),
            },
        ),
        migrations.CreateModel(
            name='TaskStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Teachers',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fname', models.CharField(max_length=20, verbose_name=b'\xd0\x98\xd0\xbc\xd1\x8f')),
                ('sname', models.CharField(max_length=20, verbose_name=b'\xd0\x9e\xd1\x82\xd1\x87\xd0\xb5\xd1\x81\xd1\x82\xd0\xb2\xd0\xbe')),
                ('lname', models.CharField(max_length=20, verbose_name=b'\xd0\xa4\xd0\xb0\xd0\xbc\xd0\xb8\xd0\xbb\xd0\xb8\xd1\x8f')),
                ('degree', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name=b'\xd0\xa3\xd1\x87\xd1\x91\xd0\xbd\xd0\xb0\xd1\x8f \xd1\x81\xd1\x82\xd0\xb5\xd0\xbf\xd0\xb5\xd0\xbd\xd1\x8c', to='prakt.AcademicDegree', null=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name=b'\xd0\x94\xd0\xbe\xd0\xbb\xd0\xb6\xd0\xbd\xd0\xbe\xd1\x81\xd1\x82\xd1\x8c', to='prakt.Posts', null=True)),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name=b'\xd0\xa3\xd1\x87\xd1\x91\xd0\xbd\xd0\xbe\xd0\xb5 \xd0\xb7\xd0\xb2\xd0\xb0\xd0\xbd\xd0\xb8\xd0\xb5', to='prakt.AcademicStatus', null=True)),
            ],
            options={
                'ordering': ('lname',),
            },
        ),
        migrations.AddField(
            model_name='tasks',
            name='status',
            field=models.ForeignKey(verbose_name=b'\xd0\xa1\xd1\x82\xd0\xb0\xd1\x82\xd1\x83\xd1\x81', to='prakt.TaskStatus'),
        ),
        migrations.AddField(
            model_name='events',
            name='org',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name=b'\xd0\x9e\xd1\x80\xd0\xb3\xd0\xb0\xd0\xbd\xd0\xb8\xd0\xb7\xd0\xb0\xd1\x86\xd0\xb8\xd1\x8f', to='prakt.Org', null=True),
        ),
        migrations.AddField(
            model_name='events',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name=b'\xd0\x9a\xd0\xbe\xd0\xbd\xd1\x82\xd0\xb0\xd0\xba\xd1\x82\xd0\xbd\xd0\xbe\xd0\xb5 \xd0\xbb\xd0\xb8\xd1\x86\xd0\xbe', blank=True, to='prakt.Employee', null=True),
        ),
        migrations.AddField(
            model_name='events',
            name='type',
            field=models.ForeignKey(verbose_name=b'\xd0\xa2\xd0\xb8\xd0\xbf \xd1\x81\xd0\xbe\xd0\xb1\xd1\x8b\xd1\x82\xd0\xb8\xd1\x8f', to='prakt.EventType'),
        ),
        migrations.AddField(
            model_name='employee',
            name='org',
            field=models.ForeignKey(verbose_name=b'\xd0\x9e\xd1\x80\xd0\xb3\xd0\xb0\xd0\xbd\xd0\xb8\xd0\xb7\xd0\xb0\xd1\x86\xd0\xb8\xd1\x8f', to='prakt.Org'),
        ),
        migrations.AddField(
            model_name='docs',
            name='org',
            field=models.ForeignKey(verbose_name=b'\xd0\x9e\xd1\x80\xd0\xb3\xd0\xb0\xd0\xbd\xd0\xb8\xd0\xb7\xd0\xb0\xd1\x86\xd0\xb8\xd1\x8f', to='prakt.Org'),
        ),
    ]
