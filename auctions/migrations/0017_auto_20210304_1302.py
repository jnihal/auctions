# Generated by Django 3.1.5 on 2021-03-04 13:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0016_auto_20210304_1114'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='listing',
            name='current_bid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='current_bids', to='auctions.bid'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='starting_bid',
            field=models.IntegerField(),
        ),
    ]