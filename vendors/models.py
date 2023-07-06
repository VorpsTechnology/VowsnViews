from django.db import models
from datetime import date, timedelta

from users.models import Vendor

YES_NO_CHOICES = (
    ('Yes', 'Yes'),
    ('No', 'No'),
)

VEG_MENU_CHOICES = (
    ('Under ₹500', 'Under ₹500'),
    ('₹ 500 - ₹ 799', '₹ 500 - ₹ 799'),
    ('₹ 700 - ₹ 999', '₹ 700 - ₹ 999'),
    ('₹ 1000 - ₹ 1499', '₹ 1000 - ₹ 1499'),
    ('₹ 1400 - ₹ 1599', '₹ 1400 - ₹ 1599'),
    ('₹ 1600 - ₹ 1799', '₹ 1600 - ₹ 1799'),
)

NONVEG_MENU_CHOICES = (
    ('₹ 1200 - ₹ 1499', '₹ 1200 - ₹ 1499'),
    ('₹ 1400 - ₹ 1599', '₹ 1400 - ₹ 1599'),
    ('₹ 1600 - ₹ 1799', '₹ 1600 - ₹ 1799'),
)

RENTAL_PRICING = (
    ('₹ 50,000 - ₹ 1,00,499', '₹ 50,000 - ₹ 10499'),
    ('₹ 60,000 - ₹ 1,10,999', '₹ 60,000 - ₹ 1,10,999'),
)

GIFTS_PRICE_RANGE = (
    ('₹ 200 - ₹ 499', '₹ 200 - ₹ 499'),
    ('₹ 500 - ₹ 999', '₹ 500 - ₹ 999'),
    ('₹ 999 - ₹ 1499', '₹ 999 - ₹ 1499'),
    ('₹ 1499 - ₹ 1999', '₹ 1499 - ₹ 1999'),
)

PRICE_PER_PERSON_MAKEUP = (
    ('₹ 500 - ₹ 1,000', '₹ 500 - ₹ 1,000'),
    ('₹ 1,500 - ₹ 2,500', '₹ 1,500 - ₹ 2,500'),
    ('₹ 5,000 - ₹ 9,999', '₹ 5,000 - ₹ 9,999'),
)

WEAR_DELIEVER_DAYS = (
    ('10-15 days', '10-15 days'),
    ('15-30 days', '15-30 days'),
    ('30-45 days', '30-45 days'),
    ('45-60 days', '45-60 days'),

)

WEAR_PRICE_RANGE = (
    ('₹ 5,000 - ₹ 9,999', '₹ 5,000 - ₹ 9,999'),
    ('₹ 10,000 - ₹ 14,999', '₹ 10,000 - ₹ 14,999'),
    ('₹ 15,000 - ₹ 19,999', '₹ 15,000 - ₹ 19,999'),
    ('₹ 20,000 - ₹ 29,999', '₹ 20,000 - ₹ 29,999'),
    ('₹ 30,000 - ₹ 39,999', '₹ 30,000 - ₹ 39,999'),
    ('₹ 40,000 - ₹ 49,999', '₹ 40,000 - ₹ 49,999'),
    ('₹ 50,000 - ₹ 59,999', '₹ 50,000 - ₹ 59,999'),
    ('₹ 60,000 - More', '₹ 60,000 - More'),

)

DECOR_PRICE_RANGE = (
    ('₹ 25,000 - ₹ 50,999', '₹ 25,000 - ₹ 50,999'),
    ('₹ 50,000 - ₹ 75,999', '₹ 50,000 - ₹ 75,999'),
    ('₹ 75,000 - ₹ 99,999', '₹ 75,000 - ₹ 99,999'),
    ('₹ 1,75,000 - ₹ 1,99,999', '₹ 1,75,000 - ₹ 1,99,999'),
    ('₹ 2,00,000 - ₹ 2,25,000', '₹ 2,00,000 - ₹ 2,25,000'),
    ('₹ 2,25,000 - ₹ 2,50,000', '₹ 2,25,000 - ₹ 2,50,000'),

)

INVITATION_PRICE_RANGE = (
    ('₹ 0 - ₹ 49', '₹ 0 - ₹ 49'),
    ('₹ 100 - ₹ 199', '₹ 100 - ₹ 199'),
    ('₹ 200 - ₹ 299', '₹ 200 - ₹ 299'),
    ('₹ 400 - ₹ 399', '₹ 300 - ₹ 399'),
    ('₹ 400 - ₹ 499', '₹ 400 - ₹ 499'),
    ('₹ 400 - More', '₹ 400 - More'),

)

MIN_QTY = (
    ('0 - 19', '0 - 19'),
    ('25 - 49', '25 - 49'),
    ('50 - 100', '50 - 100'),
    ('125 and more', '125 and more'),
)


# method to return choices for established year question
def year_choices():
    return [(r, r) for r in range(1980, date.today().year + 1)]


class FoodMenuChoices(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class SpacesTypes(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class ServicesChoices(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ExternalVendors(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class PaymentChoices(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class GuestChoices(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class PromotionOffer(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class BridalWearWorks(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class GroomWearWorks(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class FabricCollection(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class WearCategory(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class WearOccasions(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class PhotoboothTypes(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class DecorationTheme(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class VenueFAQ(models.Model):
    listing = models.ForeignKey('listing.Listing', on_delete=models.CASCADE, null=True, blank=True)
    draft_listing = models.ForeignKey('listing.DraftListing', on_delete=models.CASCADE, null=True, blank=True)
    Q1 = models.CharField(default="What is the price per plate for a wedding event ?", max_length=200)
    ans1 = models.IntegerField(blank=True, null=True)
    Q2 = models.CharField(default='What are the food menu & catering options available ?', max_length=200)
    ans2 = models.ManyToManyField(FoodMenuChoices, null=True, blank=True)
    Q3 = models.CharField(default='What kind of event spaces does have ?', max_length=200)
    ans3 = models.ManyToManyField(SpacesTypes, null=True, blank=True)
    Q4 = models.CharField(max_length=200, default='What services and amenities can provide for an event ?')
    ans4 = models.ManyToManyField(ServicesChoices, null=True, blank=True)
    Q5 = models.CharField(max_length=200, default='can provide in house vendors for additional services')
    ans5 = models.CharField(max_length=30, choices=YES_NO_CHOICES, null=True, blank=True)
    Q6 = models.CharField(max_length=200, default='Does allow external vendors for wedding and other events at venue ?')
    ans6 = models.ManyToManyField(ExternalVendors, null=True, blank=True)
    Q7 = models.CharField(max_length=200, default='Which forms of payment are accepted ?')
    ans7 = models.ManyToManyField(PaymentChoices, null=True, blank=True)
    Q8 = models.CharField(max_length=200, default='How many people can serve at a wedding event ?')
    ans8 = models.ManyToManyField(GuestChoices, null=True, blank=True)
    Q9 = models.CharField(max_length=200, default='What kind of promotions does offer ?')
    ans9 = models.ManyToManyField(PromotionOffer, null=True, blank=True)
    Q10 = models.CharField(max_length=200, default='Is alcohol permitted at your venue ?')
    ans10 = models.CharField(max_length=30, choices=YES_NO_CHOICES, null=True, blank=True)
    Q11 = models.CharField(max_length=200, default='What is the % advance payment to confirm the booking')
    ans11 = models.IntegerField(blank=True, null=True)
    Q12 = models.CharField(max_length=200,
                           default='What is the price range of veg menu for 300 PAX? (Typically includes charges for: '
                                   'beverages, food appetizers, main course & dessert items)')
    ans12 = models.CharField(max_length=100, choices=VEG_MENU_CHOICES, null=True, blank=True)
    Q13 = models.CharField(max_length=200,
                           default='What is the price range of non-veg menu for 300 PAX? (Typically includes charges '
                                   'for: beverages, food appetizers, main course & dessert items)')
    ans13 = models.CharField(max_length=100, choices=NONVEG_MENU_CHOICES, null=True, blank=True)
    Q14 = models.CharField(max_length=200, default='What is your rental only pricing range per day ?')
    ans14 = models.CharField(max_length=100, choices=RENTAL_PRICING, null=True, blank=True)

    def __str__(self):
        return f"{self.id}"


class MakeupFAQ(models.Model):
    listing = models.ForeignKey('listing.Listing', on_delete=models.CASCADE, null=True, blank=True)
    draft_listing = models.ForeignKey('listing.DraftListing', on_delete=models.CASCADE, null=True, blank=True)
    Q1 = models.CharField(max_length=200, default='Do you travel outstation?')
    ans1 = models.CharField(max_length=30, choices=YES_NO_CHOICES, null=True, blank=True)
    Q2 = models.CharField(max_length=200, default='Do you own a salon for your services?')
    ans2 = models.CharField(max_length=30, choices=YES_NO_CHOICES, null=True, blank=True)
    Q3 = models.CharField(max_length=200, default='Which forms of payment do you accept?')
    ans3 = models.ManyToManyField(PaymentChoices, null = True, blank = True)
    Q4 = models.CharField(max_length=200, default='What is the percentage payment/amount to confirm the booking?')
    ans4 = models.IntegerField(null=True, blank=True)
    Q5 = models.CharField(max_length=200, default='What is the cancellation policy of your services?')
    ans5 = models.TextField(null=True, blank=True)
    Q6 = models.TextField(max_length=200, default='What is the price per person range for bridal makeup? (Typically '
                                                  'includes: HD or Airbrush makeup with styling, draping, '
                                                  '& extensions)')
    ans6 = models.CharField(max_length=100, choices=PRICE_PER_PERSON_MAKEUP, null=True, blank=True)
    Q7 = models.TextField(max_length=200, default='What is the price per person range for party makeup for bride? ('
                                                  'Typically includes: HD makeup with styling, draping, & extensions)')
    ans7 = models.CharField(max_length=100, choices=PRICE_PER_PERSON_MAKEUP, null=True, blank=True)
    Q8 = models.TextField(default='What is the price per person range for regular party makeup for '
                                  'bride\'s relatives/ friends? (Typically includes: regular party '
                                  'makeup with styling, draping and extensions)')
    ans8 = models.CharField(max_length=100, choices=PRICE_PER_PERSON_MAKEUP, null=True, blank=True)

    def __str__(self):
        return f"{self.id}"


class BridalWearFAQ(models.Model):
    listing = models.ForeignKey('listing.Listing', on_delete=models.CASCADE, null=True, blank=True)
    draft_listing = models.ForeignKey('listing.DraftListing', on_delete=models.CASCADE, null=True, blank=True)
    Q1 = models.CharField(max_length=200, default='What kind of work do you have on your bridal wear?')
    ans1 = models.ManyToManyField(BridalWearWorks, null = True, blank = True)
    Q2 = models.CharField(max_length=200, default='What are the fabrics of the bridal wear in your collection?')
    ans2 = models.ManyToManyField(FabricCollection, null = True, blank = True)
    Q3 = models.CharField(max_length=200, default='What all wedding collection categories do you have?')
    ans3 = models.ManyToManyField(WearCategory, null = True, blank = True)
    Q4 = models.CharField(max_length=200, default='Do you require customers to book an appointment?')
    ans4 = models.CharField(max_length=30, choices=YES_NO_CHOICES, null=True, blank=True)
    Q5 = models.CharField(max_length=200, default='How much time do you take to deliver the final bridal wear?')
    ans5 = models.CharField(max_length=50, choices=WEAR_DELIEVER_DAYS, null=True, blank=True)
    Q6 = models.CharField(max_length=200, default='Do you take customized designs for order?')
    ans6 = models.CharField(max_length=30, choices=YES_NO_CHOICES, null=True, blank=True)
    Q7 = models.CharField(max_length=200, default='Do you ship products outstation?')
    ans7 = models.CharField(max_length=30, choices=YES_NO_CHOICES, null=True, blank=True)
    Q8 = models.CharField(max_length=200, default='Which forms of payment do you accept?')
    ans8 = models.ManyToManyField(PaymentChoices, null = True, blank = True)
    Q9 = models.CharField(max_length=200, default='What is the percentage payment / amount to confirm the booking?')
    ans9 = models.IntegerField(null=True, blank=True)
    Q10 = models.CharField(max_length=200, default='What is the cancellation policy?')
    ans10 = models.TextField(null=True, blank=True)
    Q11 = models.CharField(max_length=200,
                           default='Which year did you/your company professionally start your services?')
    ans11 = models.IntegerField(choices=year_choices(), null=True, blank=True)
    Q12 = models.CharField(max_length=200, default='Awards, recognitions and publications:')
    ans12 = models.CharField(null=True, blank=True, max_length=100)
    Q13 = models.CharField(max_length=200, default='What is the starting price range of bridal lehenga?')
    ans13 = models.CharField(max_length=100, choices=WEAR_PRICE_RANGE, null=True, blank=True)

    def __str__(self):
        return f"{self.id}"


class GroomWearFAQ(models.Model):
    listing = models.ForeignKey('listing.Listing', on_delete=models.CASCADE, null=True, blank=True)
    draft_listing = models.ForeignKey('listing.DraftListing', on_delete=models.CASCADE, null=True, blank=True)
    Q1 = models.CharField(max_length=200, default='What are the work that you have on groom wear collection?')
    ans1 = models.ManyToManyField(GroomWearWorks, null = True, blank = True)
    Q2 = models.CharField(max_length=200, default='What are the fabrics of the groom wear in your collection?')
    ans2 = models.ManyToManyField(FabricCollection, null = True, blank = True)
    Q3 = models.CharField(max_length=200, default='What are the occasion wear collection that you specialize in?')
    ans3 = models.ManyToManyField(WearOccasions, null = True, blank = True)
    Q4 = models.CharField(max_length=200, default='What all wedding collection categories do you have?')
    ans4 = models.ManyToManyField(WearCategory, null = True, blank = True)
    Q5 = models.CharField(max_length=200, default='How much time do you take to deliver the final groom wear?')
    ans5 = models.CharField(max_length=50, choices=WEAR_DELIEVER_DAYS, null=True, blank=True)
    Q6 = models.CharField(max_length=200, default='Do you take customized designs for order?')
    ans6 = models.CharField(max_length=30, choices=YES_NO_CHOICES, null=True, blank=True)
    Q7 = models.CharField(max_length=200, default='Do you ship products outstation?')
    ans7 = models.CharField(max_length=30, choices=YES_NO_CHOICES, null=True, blank=True)
    Q8 = models.CharField(max_length=200, default='Which forms of payment do you accept?')
    ans8 = models.ManyToManyField(PaymentChoices, null = True, blank = True)
    Q9 = models.CharField(max_length=200, default='What is the percentage payment / amount to confirm the booking?')
    ans9 = models.IntegerField(null=True, blank=True)
    Q10 = models.CharField(max_length=200, default='What is the cancellation policy?')
    ans10 = models.TextField(null=True, blank=True)
    Q11 = models.CharField(max_length=200,
                           default='Which year did you/your company professionally start your services?')
    ans11 = models.IntegerField(choices=year_choices(), null=True, blank=True)
    Q12 = models.CharField(max_length=200, default='Awards, recognitions and publications:')
    ans12 = models.CharField(null=True, blank=True, max_length=100)
    Q13 = models.CharField(max_length=200, default='What is the starting price range of groom wear?')
    ans13 = models.CharField(max_length=100, choices=WEAR_PRICE_RANGE, null=True, blank=True)

    def __str__(self):
        return f"{self.id}"


class PhotographerFAQ(models.Model):
    listing = models.ForeignKey('listing.Listing', on_delete=models.CASCADE, null=True, blank=True)
    draft_listing = models.ForeignKey('listing.DraftListing', on_delete=models.CASCADE, null=True, blank=True)
    Q1 = models.CharField(max_length=200,
                          default='What is the starting price range of your photobooth installation for one event?')
    ans1 = models.IntegerField(null=True, blank=True)
    Q2 = models.CharField(max_length=200, default='What kind of photobooth can design or offer at the event?')
    ans2 = models.ManyToManyField(PhotoboothTypes, null = True, blank = True)
    Q3 = models.CharField(max_length=200, default='Which forms of payment do you accept?')
    ans3 = models.ManyToManyField(PaymentChoices, null = True, blank = True)
    Q4 = models.CharField(max_length=200, default='What is the percentage payment/ amount to confirm the booking?')
    ans4 = models.IntegerField(null=True, blank=True)
    Q5 = models.CharField(max_length=200, default='Which year did you/your company professionally start your services?')
    ans5 = models.IntegerField(choices=year_choices(), null=True, blank=True)
    Q6 = models.CharField(max_length=200, default='What is the cancellation policy?')
    ans6 = models.TextField(null=True, blank=True)
    Q7 = models.CharField(max_length=200, default='Awards, recognitions and publications:')
    ans7 = models.CharField(null=True, blank=True, max_length=100)

    def __str__(self):
        return f"{self.id}"


class DecorFAQ(models.Model):
    listing = models.ForeignKey('listing.Listing', on_delete=models.CASCADE, null=True, blank=True)
    draft_listing = models.ForeignKey('listing.DraftListing', on_delete=models.CASCADE, null=True, blank=True)
    Q1 = models.TextField(default='What is the price for flower based traditional decoration for an outdoor setup for '
                                  '300 PAX? (Typically includes decoration of: entrance, passage, guest area, '
                                  'stage area, mandapa)')
    ans1 = models.IntegerField(null=True, blank=True)
    Q2 = models.CharField(max_length=200, default='What all modern themes of decoration can you fulfil?')
    ans2 = models.ManyToManyField(DecorationTheme, null = True, blank = True)
    Q3 = models.CharField(max_length=200, default='Which forms of payment do you accept?')
    ans3 = models.ManyToManyField(PaymentChoices, null = True, blank = True)
    Q4 = models.CharField(max_length=200, default='What is the percentage payment/ amount to confirm the booking?')
    ans4 = models.IntegerField(null=True, blank=True)
    Q5 = models.CharField(max_length=200, default='What is the cancellation policy?')
    ans5 = models.TextField(null=True, blank=True)
    Q6 = models.CharField(max_length=200, default='Which year did you/your company professionally start your services?')
    ans6 = models.IntegerField(choices=year_choices(), null=True, blank=True)
    Q7 = models.CharField(max_length=200, default='Awards, recognitions and publications:')
    ans7 = models.CharField(null=True, blank=True, max_length=100)
    Q8 = models.TextField(
        default='What is the price range for flower based traditional decoration for an indoor venue setup for 100 '
                'PAX for pre-wedding/ reception events? (Typically includes decoration of: entrance-8x8 ft, passage, '
                'guest area, stage area-16x12 ft)?')
    ans8 = models.CharField(choices=DECOR_PRICE_RANGE, max_length=100, null=True, blank=True)
    Q9 = models.TextField(
        default='What is the price range for flower based traditional decoration for an outdoor setup for 300 PAX for '
                'wedding events? (Typically includes decoration of: entrance, passage, guest area, stage area, '
                'mandapa)')
    ans9 = models.CharField(choices=DECOR_PRICE_RANGE, max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.id}"


class InvitationFAQ(models.Model):
    listing = models.ForeignKey('listing.Listing', on_delete=models.CASCADE, null=True, blank=True)
    draft_listing = models.ForeignKey('listing.DraftListing', on_delete=models.CASCADE, null=True, blank=True)
    Q1 = models.CharField(max_length=200, default='What is the minimum order quantity for printed cards?')
    ans1 = models.IntegerField(null=True, blank=True)
    Q2 = models.CharField(max_length=200, default='What is the minimum order quantity for boxed invites?')
    ans2 = models.IntegerField(null=True, blank=True)
    Q3 = models.CharField(max_length=200, default='What kind of invitation concepts do you provide?')
    ans3 = models.CharField(max_length=100, null=True, blank=True)
    Q4 = models.CharField(max_length=200, default='Which forms of payment do you accept?')
    ans4 = models.ManyToManyField(PaymentChoices, null = True, blank = True)
    Q5 = models.CharField(max_length=200, default='What is the percentage payment/ amount to confirm the booking?')
    ans5 = models.IntegerField(null=True, blank=True)
    Q6 = models.CharField(max_length=200, default='What is the cancellation policy?')
    ans6 = models.TextField(null=True, blank=True)
    Q7 = models.CharField(max_length=200, default='Which year did you/your company professionally start your services?')
    ans7 = models.IntegerField(choices=year_choices(), null=True, blank=True)
    Q8 = models.CharField(max_length=200, default='What is the starting price range per invite for wedding cards?')
    ans8 = models.CharField(choices=INVITATION_PRICE_RANGE, max_length=100, null=True, blank=True)
    Q9 = models.CharField(max_length=200, default='What is the minimum order quantity range for printed cards?')
    ans9 = models.CharField(choices=MIN_QTY, max_length=100, null=True, blank=True)
    Q10 = models.CharField(max_length=200,
                           default='What is the minimum order quantity range for packaged (boxed) invitations?')
    ans10 = models.CharField(choices=MIN_QTY, max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.id}"


class GiftsFAQ(models.Model):
    listing = models.ForeignKey('listing.Listing', on_delete=models.CASCADE, null=True, blank=True)
    draft_listing = models.ForeignKey('listing.DraftListing', on_delete=models.CASCADE, null=True, blank=True)
    Q1 = models.CharField(max_length=200, default='What is the minimum order quantity for edible gifting or favors?')
    ans1 = models.IntegerField(null=True, blank=True)
    Q2 = models.CharField(max_length=200,
                          default='What is the minimum order quantity for non-edible gifting or favors?')
    ans2 = models.IntegerField(null=True, blank=True)
    Q3 = models.CharField(max_length=200, default='Which forms of payment do you accept?')
    ans3 = models.ManyToManyField(PaymentChoices, null = True, blank = True)
    Q4 = models.CharField(max_length=200, default='What is the percentage payment/ amount to confirm the booking?')
    ans4 = models.IntegerField(null=True, blank=True)
    Q5 = models.CharField(max_length=200, default='What is the cancellation policy?')
    ans5 = models.TextField(null=True, blank=True)
    Q6 = models.CharField(max_length=200, default='Which year did you/your company professionally start your services?')
    ans6 = models.IntegerField(choices=year_choices(), null=True, blank=True)
    Q7 = models.CharField(max_length=200,
                          default='What is the starting price range per kg for edible gifting or favors? (Typically '
                                  'includes: Sweets or chocolates)')
    ans7 = models.CharField(choices=GIFTS_PRICE_RANGE, max_length=100, null=True, blank=True)
    Q8 = models.CharField(max_length=200,
                          default='What is the starting price range per gift/ pack for non-edible gifting or favors?')
    ans8 = models.CharField(choices=GIFTS_PRICE_RANGE, max_length=100, null=True, blank=True)
    Q9 = models.CharField(max_length=200,
                          default='What is the minimum order quantity range for edible gifting or favors?')
    ans9 = models.CharField(choices=MIN_QTY, max_length=100, null=True, blank=True)
    Q10 = models.CharField(max_length=200,
                           default='What is the minimum order quantity range for non-edible gifting or favors?')
    ans10 = models.CharField(choices=MIN_QTY, max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.id}"


class VendorInstagramToken(models.Model):
    vendor = models.OneToOneField(Vendor, on_delete=models.CASCADE)
    token = models.TextField()
    date_added = models.DateField()

    def __str__(self):
        return f"{self.id}"

    def days_remaining(self):
        exp_date = self.date_added + timedelta(58)
        day = exp_date - self.date_added
        return day.days