# Generated by Django 3.2.23 on 2024-01-24 02:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news_app', '0006_auto_20240115_0957'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='news',
            name='description_vi',
        ),
        migrations.RemoveField(
            model_name='news',
            name='title_vi',
        ),
    ]