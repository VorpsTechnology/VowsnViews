from django.contrib import admin
from .models import ( FoodMenuChoices, SpacesTypes, ServicesChoices, ExternalVendors, PaymentChoices,
                      GuestChoices, PromotionOffer, BridalWearWorks, GroomWearWorks, FabricCollection,
                      WearCategory, WearOccasions, PhotoboothTypes, DecorationTheme, VenueFAQ,
                      MakeupFAQ, BridalWearFAQ, GroomWearFAQ, PhotographerFAQ, DecorFAQ,
                      InvitationFAQ, GiftsFAQ, VendorInstagramToken
                     )

# Register your models here.

admin.site.register(VenueFAQ)
admin.site.register(VendorInstagramToken)
admin.site.register(MakeupFAQ)
admin.site.register(BridalWearFAQ)
admin.site.register(GroomWearFAQ)
admin.site.register(PhotographerFAQ)
admin.site.register(DecorFAQ)
admin.site.register(InvitationFAQ)
admin.site.register(GiftsFAQ)

admin.site.register(FoodMenuChoices)
admin.site.register(SpacesTypes)
admin.site.register(ServicesChoices)
admin.site.register(ExternalVendors)
admin.site.register(PaymentChoices)
admin.site.register(GuestChoices)
admin.site.register(PromotionOffer)
admin.site.register(BridalWearWorks)
admin.site.register(GroomWearWorks)
admin.site.register(FabricCollection)
admin.site.register(WearCategory)
admin.site.register(WearOccasions)
admin.site.register(PhotoboothTypes)
admin.site.register(DecorationTheme)


