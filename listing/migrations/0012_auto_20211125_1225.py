# Generated by Django 3.1.3 on 2021-11-25 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listing', '0011_auto_20211125_1205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='draftlisting',
            name='photos',
            field=models.ManyToManyField(blank=True, null=True, to='listing.ListingPhoto'),
        ),
        migrations.AlterField(
            model_name='draftlisting',
            name='videos',
            field=models.ManyToManyField(blank=True, null=True, to='listing.ListingVideo'),
        ),
    ]
