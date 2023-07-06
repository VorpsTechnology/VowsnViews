# Generated by Django 3.1.3 on 2021-07-27 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bridalwearfaq',
            name='ans1',
            field=models.ManyToManyField(blank=True, null=True, to='vendors.BridalWearWorks'),
        ),
        migrations.AlterField(
            model_name='bridalwearfaq',
            name='ans2',
            field=models.ManyToManyField(blank=True, null=True, to='vendors.FabricCollection'),
        ),
        migrations.AlterField(
            model_name='bridalwearfaq',
            name='ans3',
            field=models.ManyToManyField(blank=True, null=True, to='vendors.WearCategory'),
        ),
        migrations.AlterField(
            model_name='bridalwearfaq',
            name='ans5',
            field=models.CharField(blank=True, choices=[('10-15 days', '10-15 days'), ('15-30 days', '15-30 days'), ('30-45 days', '30-45 days'), ('45-60 days', '45-60 days')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='bridalwearfaq',
            name='ans8',
            field=models.ManyToManyField(blank=True, null=True, to='vendors.PaymentChoices'),
        ),
        migrations.AlterField(
            model_name='decorfaq',
            name='ans2',
            field=models.ManyToManyField(blank=True, null=True, to='vendors.DecorationTheme'),
        ),
        migrations.AlterField(
            model_name='decorfaq',
            name='ans3',
            field=models.ManyToManyField(blank=True, null=True, to='vendors.PaymentChoices'),
        ),
        migrations.AlterField(
            model_name='giftsfaq',
            name='ans3',
            field=models.ManyToManyField(blank=True, null=True, to='vendors.PaymentChoices'),
        ),
        migrations.AlterField(
            model_name='groomwearfaq',
            name='ans1',
            field=models.ManyToManyField(blank=True, null=True, to='vendors.GroomWearWorks'),
        ),
        migrations.AlterField(
            model_name='groomwearfaq',
            name='ans2',
            field=models.ManyToManyField(blank=True, null=True, to='vendors.FabricCollection'),
        ),
        migrations.AlterField(
            model_name='groomwearfaq',
            name='ans3',
            field=models.ManyToManyField(blank=True, null=True, to='vendors.WearOccasions'),
        ),
        migrations.AlterField(
            model_name='groomwearfaq',
            name='ans4',
            field=models.ManyToManyField(blank=True, null=True, to='vendors.WearCategory'),
        ),
        migrations.AlterField(
            model_name='groomwearfaq',
            name='ans5',
            field=models.CharField(blank=True, choices=[('10-15 days', '10-15 days'), ('15-30 days', '15-30 days'), ('30-45 days', '30-45 days'), ('45-60 days', '45-60 days')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='groomwearfaq',
            name='ans8',
            field=models.ManyToManyField(blank=True, null=True, to='vendors.PaymentChoices'),
        ),
        migrations.AlterField(
            model_name='invitationfaq',
            name='ans4',
            field=models.ManyToManyField(blank=True, null=True, to='vendors.PaymentChoices'),
        ),
        migrations.AlterField(
            model_name='makeupfaq',
            name='ans3',
            field=models.ManyToManyField(blank=True, null=True, to='vendors.PaymentChoices'),
        ),
        migrations.AlterField(
            model_name='photographerfaq',
            name='ans2',
            field=models.ManyToManyField(blank=True, null=True, to='vendors.PhotoboothTypes'),
        ),
        migrations.AlterField(
            model_name='photographerfaq',
            name='ans3',
            field=models.ManyToManyField(blank=True, null=True, to='vendors.PaymentChoices'),
        ),
        migrations.AlterField(
            model_name='venuefaq',
            name='Q11',
            field=models.CharField(default='What is the % advance payment to confirm the booking', max_length=200),
        ),
        migrations.AlterField(
            model_name='venuefaq',
            name='ans2',
            field=models.ManyToManyField(blank=True, null=True, to='vendors.FoodMenuChoices'),
        ),
        migrations.AlterField(
            model_name='venuefaq',
            name='ans3',
            field=models.ManyToManyField(blank=True, null=True, to='vendors.SpacesTypes'),
        ),
        migrations.AlterField(
            model_name='venuefaq',
            name='ans4',
            field=models.ManyToManyField(blank=True, null=True, to='vendors.ServicesChoices'),
        ),
        migrations.AlterField(
            model_name='venuefaq',
            name='ans6',
            field=models.ManyToManyField(blank=True, null=True, to='vendors.ExternalVendors'),
        ),
        migrations.AlterField(
            model_name='venuefaq',
            name='ans7',
            field=models.ManyToManyField(blank=True, null=True, to='vendors.PaymentChoices'),
        ),
        migrations.AlterField(
            model_name='venuefaq',
            name='ans8',
            field=models.ManyToManyField(blank=True, null=True, to='vendors.GuestChoices'),
        ),
        migrations.AlterField(
            model_name='venuefaq',
            name='ans9',
            field=models.ManyToManyField(blank=True, null=True, to='vendors.PromotionOffer'),
        ),
    ]
