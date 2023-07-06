# Generated by Django 3.1.3 on 2021-07-27 08:13

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AddititionalPricing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pricing_title', models.CharField(default='No Additional Cost', max_length=100)),
                ('cost', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('suffix', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seating_type', models.CharField(choices=[('Indoor', 'Indoor'), ('Outdoor', 'Outdoor')], max_length=20)),
                ('seating_space', models.IntegerField()),
                ('floating_space', models.IntegerField()),
                ('additional_text', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='area')),
            ],
        ),
        migrations.CreateModel(
            name='DraftListing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('low_price', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('high_price', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('price_for', models.CharField(blank=True, max_length=500, null=True)),
                ('pre_low_price_text', models.CharField(blank=True, max_length=500, null=True)),
                ('post_low_price_text', models.CharField(blank=True, max_length=500, null=True)),
                ('pre_high_price_text', models.CharField(blank=True, max_length=500, null=True)),
                ('post_high_price_text', models.CharField(blank=True, max_length=500, null=True)),
                ('additional_text', ckeditor.fields.RichTextField(blank=True, help_text='To describe product price', null=True)),
                ('slug', models.SlugField(unique=True)),
                ('meta_title', models.TextField(blank=True, null=True)),
                ('meta_description', models.TextField(blank=True, null=True)),
                ('short_description', ckeditor.fields.RichTextField(blank=True, help_text='To describe product in short', null=True)),
                ('description', ckeditor.fields.RichTextField(blank=True, help_text='Overview product', null=True)),
                ('more_info', ckeditor.fields.RichTextField(blank=True, help_text='More Info', null=True)),
                ('is_in_house_listing', models.BooleanField(default=False)),
                ('review_id', models.CharField(blank=True, max_length=200, null=True)),
                ('address', models.TextField(blank=True, max_length=200, null=True)),
                ('image_main', models.ImageField(blank=True, null=True, upload_to='listings')),
                ('image_2', models.ImageField(blank=True, null=True, upload_to='listings')),
                ('image_3', models.ImageField(blank=True, null=True, upload_to='listings')),
                ('image_4', models.ImageField(blank=True, null=True, upload_to='listings')),
                ('image_5', models.ImageField(blank=True, null=True, upload_to='listings')),
                ('image_main_link', models.URLField(blank=True, null=True)),
                ('image_2_link', models.URLField(blank=True, null=True)),
                ('image_3_link', models.URLField(blank=True, null=True)),
                ('image_4_link', models.URLField(blank=True, null=True)),
                ('image_5_link', models.URLField(blank=True, null=True)),
                ('video_1', models.URLField(blank=True, null=True)),
                ('video_2', models.URLField(blank=True, null=True)),
                ('video_3', models.URLField(blank=True, null=True)),
                ('video_4', models.URLField(blank=True, null=True)),
                ('video_5', models.URLField(blank=True, null=True)),
                ('video_6', models.URLField(blank=True, null=True)),
                ('video_7', models.URLField(blank=True, null=True)),
                ('video_8', models.URLField(blank=True, null=True)),
                ('video_9', models.URLField(blank=True, null=True)),
                ('video_10', models.URLField(blank=True, null=True)),
                ('label', models.CharField(blank=True, choices=[('Our Recommendation', 'Our Recommendation'), ('Most Booked', 'Most Booked'), ('Trending', 'Trending'), ('Popular', 'Popular'), ('Best Deal', 'Best Deal'), ('Best Offer', 'Best Offer')], max_length=20, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_verified', models.BooleanField(default=False)),
                ('trending', models.BooleanField(default=False)),
                ('top_trending', models.BooleanField(default=False)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('catering_policy', models.CharField(blank=True, max_length=200, null=True)),
                ('decor_policy', models.CharField(blank=True, max_length=200, null=True)),
                ('alcohol_policy', models.CharField(blank=True, max_length=200, null=True)),
                ('dj_policy', models.CharField(blank=True, max_length=200, null=True)),
                ('is_approved', models.BooleanField(default=False)),
                ('is_update', models.BooleanField(default=False)),
                ('is_faq_answered', models.BooleanField(default=False)),
                ('decline_reason', models.TextField(blank=True, null=True)),
                ('is_declined', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'listings_draft_listing',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vendor_name', models.TextField(blank=True, null=True)),
                ('title', models.CharField(max_length=200, unique=True)),
                ('low_price', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('high_price', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('price_for', models.CharField(blank=True, max_length=500, null=True)),
                ('pre_low_price_text', models.CharField(blank=True, max_length=500, null=True)),
                ('post_low_price_text', models.CharField(blank=True, max_length=500, null=True)),
                ('pre_high_price_text', models.CharField(blank=True, max_length=500, null=True)),
                ('post_high_price_text', models.CharField(blank=True, max_length=500, null=True)),
                ('additional_text', ckeditor.fields.RichTextField(blank=True, help_text='To describe product price', null=True)),
                ('slug', models.SlugField(blank=True, null=True, unique=True)),
                ('meta_title', models.TextField(blank=True, null=True)),
                ('meta_description', models.TextField(blank=True, null=True)),
                ('short_description', ckeditor.fields.RichTextField(blank=True, help_text='To describe product in short', null=True)),
                ('description', ckeditor.fields.RichTextField(blank=True, help_text='Overview product', null=True)),
                ('more_info', ckeditor.fields.RichTextField(blank=True, help_text='More Info', null=True)),
                ('is_in_house_listing', models.BooleanField(default=False)),
                ('address', models.TextField(blank=True, max_length=200, null=True)),
                ('image_main', models.ImageField(blank=True, null=True, upload_to='listings')),
                ('image_2', models.ImageField(blank=True, null=True, upload_to='listings')),
                ('image_3', models.ImageField(blank=True, null=True, upload_to='listings')),
                ('image_4', models.ImageField(blank=True, null=True, upload_to='listings')),
                ('image_5', models.ImageField(blank=True, null=True, upload_to='listings')),
                ('image_main_link', models.URLField(blank=True, null=True)),
                ('image_2_link', models.URLField(blank=True, null=True)),
                ('image_3_link', models.URLField(blank=True, null=True)),
                ('image_4_link', models.URLField(blank=True, null=True)),
                ('image_5_link', models.URLField(blank=True, null=True)),
                ('video_1', models.URLField(blank=True, null=True)),
                ('video_2', models.URLField(blank=True, null=True)),
                ('video_3', models.URLField(blank=True, null=True)),
                ('video_4', models.URLField(blank=True, null=True)),
                ('video_5', models.URLField(blank=True, null=True)),
                ('video_6', models.URLField(blank=True, null=True)),
                ('video_7', models.URLField(blank=True, null=True)),
                ('video_8', models.URLField(blank=True, null=True)),
                ('video_9', models.URLField(blank=True, null=True)),
                ('video_10', models.URLField(blank=True, null=True)),
                ('label', models.CharField(blank=True, choices=[('Our Recommendation', 'Our Recommendation'), ('Most Booked', 'Most Booked'), ('Trending', 'Trending'), ('Popular', 'Popular'), ('Best Deal', 'Best Deal'), ('Best Offer', 'Best Offer')], max_length=20, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_verified', models.BooleanField(default=False)),
                ('trending', models.BooleanField(default=False)),
                ('top_trending', models.BooleanField(default=False)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('catering_policy', models.CharField(blank=True, max_length=200, null=True)),
                ('decor_policy', models.CharField(blank=True, max_length=200, null=True)),
                ('alcohol_policy', models.CharField(blank=True, max_length=200, null=True)),
                ('dj_policy', models.CharField(blank=True, max_length=200, null=True)),
                ('is_faq_answered', models.BooleanField(default=False)),
                ('place_id', models.CharField(blank=True, max_length=200, null=True)),
            ],
            options={
                'db_table': 'listings_listing',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='ListingCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, unique=True)),
                ('slug', models.SlugField(unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='listing_category')),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='ListingContact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('mobile', models.BigIntegerField()),
                ('description', models.TextField()),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('read', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='ListingFavorite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='ListingLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, unique=True)),
                ('slug', models.SlugField(unique=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='listing_location')),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='ListingPhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='listing/photos/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ListingReview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('review_description', models.TextField()),
                ('rating', models.FloatField(choices=[(1, 1), (1.5, 1.5), (2, 2), (2.5, 2.5), (3, 3), (3.5, 3.5), (4, 4), (4.5, 4.5), (5, 5)], max_length=3)),
                ('is_approved', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='ListingVideo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='listing/video/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ParentListingCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, unique=True)),
                ('slug', models.SlugField(unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='parent_listing-category')),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='SubListingLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, unique=True)),
                ('slug', models.SlugField(unique=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='listing_location')),
                ('is_active', models.BooleanField(default=True)),
                ('listing_location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='listing.listinglocation')),
            ],
        ),
    ]