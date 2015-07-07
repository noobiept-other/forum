# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import forum.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=50, unique=True)),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('text', models.TextField(max_length=1000)),
                ('was_edited', models.BooleanField(default=False)),
                ('date_created', models.DateTimeField(default=forum.models.getTime, help_text='Date Created')),
                ('date_edited', models.DateTimeField(default=forum.models.getTime, help_text='Last time the post was edited ')),
                ('edited_by', models.ForeignKey(related_name='post_edited_by', blank=True, help_text='who edited the post.', null=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SubForum',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=50, unique=True)),
                ('slug', models.SlugField(unique=True)),
                ('category', models.ForeignKey(to='forum.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Thread',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('title', models.CharField(max_length=50)),
                ('slug', models.SlugField(unique=True)),
                ('text', models.TextField(max_length=1000)),
                ('date_created', models.DateTimeField(default=forum.models.getTime, help_text='Date Created')),
                ('was_edited', models.BooleanField(default=False)),
                ('date_edited', models.DateTimeField(default=forum.models.getTime, help_text='Last time the post was edited ')),
                ('is_locked', models.BooleanField(default=False, help_text='if you can add new posts to the thread or not.')),
                ('edited_by', models.ForeignKey(related_name='thread_edited_by', blank=True, help_text='who edited the thread.', null=True, to=settings.AUTH_USER_MODEL)),
                ('sub_forum', models.ForeignKey(to='forum.SubForum')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='sub_forum',
            field=models.ForeignKey(to='forum.SubForum'),
        ),
        migrations.AddField(
            model_name='post',
            name='thread',
            field=models.ForeignKey(to='forum.Thread'),
        ),
        migrations.AddField(
            model_name='post',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
