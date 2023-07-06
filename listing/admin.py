from django.contrib import admin

from .models import Listing, ListingCategory, ListingLocation, ListingReview, ParentListingCategory, ListingContact, \
                    ListingPhoto, SubListingLocation, AddititionalPricing, Area, DraftListing

from import_export.admin import ImportExportModelAdmin


class ListingAdmin(ImportExportModelAdmin):
    pass


class ListingLocationAdmin(ImportExportModelAdmin):
    pass


class ListingCategoryAdmin(ImportExportModelAdmin):
    pass


class ParentCategoryAdmin(ImportExportModelAdmin):
    pass


admin.site.register(Listing, ListingAdmin)
admin.site.register(ListingLocation, ListingLocationAdmin)
admin.site.register(SubListingLocation)
admin.site.register(ListingCategory, ListingCategoryAdmin)
admin.site.register(ParentListingCategory, ParentCategoryAdmin)

admin.site.register(ListingReview)
admin.site.register(ListingContact)
admin.site.register(ListingPhoto)
admin.site.register(Area)
admin.site.register(AddititionalPricing)
admin.site.register(DraftListing)

