# Generated by Django 3.1.3 on 2021-09-06 14:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tpp',
            old_name='some_policy',
            new_name='vendor_policy',
        ),
    ]
