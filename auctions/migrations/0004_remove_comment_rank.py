# Generated by Django 3.2.4 on 2021-07-20 10:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_auto_20210719_2000'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='rank',
        ),
    ]
