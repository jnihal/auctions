# Generated by Django 3.1.5 on 2021-03-04 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0020_auto_20210304_1420'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='current_bid',
        ),
        migrations.AddField(
            model_name='listing',
            name='current_bid',
            field=models.IntegerField(default=0),
        ),
    ]