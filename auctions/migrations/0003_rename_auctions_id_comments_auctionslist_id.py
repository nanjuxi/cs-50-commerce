# Generated by Django 3.2.5 on 2021-09-21 08:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comments',
            old_name='auctions_id',
            new_name='auctionslist_id',
        ),
    ]