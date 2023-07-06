from django.contrib import admin
from.models import (
    Category, Product, Review, Variation, ParentCategory,FunctionCategory,ProductBrand,Gender, ProductSize, ProductColor
)
from import_export.admin import ImportExportModelAdmin


class ProductsAdmin(ImportExportModelAdmin):
    pass


class VariationAdmin(ImportExportModelAdmin):
    pass


class CategoryAdmin(ImportExportModelAdmin):
    pass


class ParentCategoryAdmin(ImportExportModelAdmin):
    pass


admin.site.register(Product, ProductsAdmin)
admin.site.register(Variation, VariationAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(ParentCategory, ParentCategoryAdmin)
admin.site.register(Review)
admin.site.register(FunctionCategory)
admin.site.register(Gender)
admin.site.register(ProductBrand)
admin.site.register(ProductSize)
admin.site.register(ProductColor)
