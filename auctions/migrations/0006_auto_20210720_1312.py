# Generated by Django 3.2.4 on 2021-07-20 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_comment_listing'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='closed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='listing',
            name='listedBy',
            field=models.CharField(default='editme', max_length=256),
            preserve_default=False,
        ),
    ]
