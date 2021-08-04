# Generated by Django 3.1.5 on 2021-03-04 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0019_auto_20210304_1416'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='current_bid',
        ),
        migrations.AddField(
            model_name='listing',
            name='current_bid',
            field=models.ManyToManyField(blank=True, related_name='current_bids', to='auctions.Bid'),
        ),
    ]