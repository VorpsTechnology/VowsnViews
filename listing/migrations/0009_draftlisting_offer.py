# Generated by Django 3.1.3 on 2021-09-11 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listing', '0008_auto_20210911_1251'),
    ]

    operations = [
        migrations.AddField(
            model_name='draftlisting',
            name='offer',
            field=models.ManyToManyField(blank=True, null=True, to='listing.ListingOffer'),
        ),
    ]
