# Generated by Django 3.1.5 on 2021-03-04 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0022_auto_20210304_1725'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='current_bid_user',
            field=models.CharField(default=None, max_length=64),
        ),
    ]