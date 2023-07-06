# Generated by Django 3.1.3 on 2021-07-27 08:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('listing', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='listingreview',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='listingfavorite',
            name='listing',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='listing.listing'),
        ),
        migrations.AddField(
            model_name='listingfavorite',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='listingcontact',
            name='listing',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='listing.listing'),
        ),
        migrations.AddField(
            model_name='listingcategory',
            name='parent_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='listing.parentlistingcategory'),
        ),
        migrations.AddField(
            model_name='listing',
            name='additional_pricing',
            field=models.ManyToManyField(blank=True, to='listing.AddititionalPricing'),
        ),
        migrations.AddField(
            model_name='listing',
            name='area',
            field=models.ManyToManyField(blank=True, to='listing.Area'),
        ),
        migrations.AddField(
            model_name='listing',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='listing.listingcategory'),
        ),
        migrations.AddField(
            model_name='listing',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='listing.listinglocation'),
        ),
        migrations.AddField(
            model_name='listing',
            name='parent_category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='listing.parentlistingcategory'),
        ),
        migrations.AddField(
            model_name='listing',
            name='photos',
            field=models.ManyToManyField(to='listing.ListingPhoto'),
        ),
        migrations.AddField(
            model_name='listing',
            name='review',
            field=models.ManyToManyField(blank=True, to='listing.ListingReview'),
        ),
        migrations.AddField(
            model_name='listing',
            name='sub_location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='listing.sublistinglocation'),
        ),
        migrations.AddField(
            model_name='listing',
            name='videos',
            field=models.ManyToManyField(to='listing.ListingVideo'),
        ),
        migrations.AddField(
            model_name='draftlisting',
            name='additional_pricing',
            field=models.ManyToManyField(blank=True, to='listing.AddititionalPricing'),
        ),
        migrations.AddField(
            model_name='draftlisting',
            name='area',
            field=models.ManyToManyField(blank=True, to='listing.Area'),
        ),
        migrations.AddField(
            model_name='draftlisting',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='listing.listingcategory'),
        ),
        migrations.AddField(
            model_name='draftlisting',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='listing.listinglocation'),
        ),
        migrations.AddField(
            model_name='draftlisting',
            name='parent_category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='listing.parentlistingcategory'),
        ),
        migrations.AddField(
            model_name='draftlisting',
            name='photos',
            field=models.ManyToManyField(to='listing.ListingPhoto'),
        ),
        migrations.AddField(
            model_name='draftlisting',
            name='review',
            field=models.ManyToManyField(blank=True, to='listing.ListingReview'),
        ),
        migrations.AddField(
            model_name='draftlisting',
            name='sub_location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='listing.sublistinglocation'),
        ),
        migrations.AddField(
            model_name='draftlisting',
            name='videos',
            field=models.ManyToManyField(to='listing.ListingVideo'),
        ),
    ]
