# Generated by Django 3.1.3 on 2021-09-10 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listing', '0006_listing_review_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='ListingOffer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('offer_title', models.CharField(blank=True, max_length=300, null=True)),
                ('offer_description', models.TextField(blank=True, null=True)),
                ('offer_expires', models.DateField(blank=True, null=True)),
                ('offer_image', models.ImageField(blank=True, null=True, upload_to='')),
            ],
        ),
        migrations.AddField(
            model_name='listing',
            name='offer',
            field=models.ManyToManyField(blank=True, null=True, to='listing.ListingOffer'),
        ),
    ]
