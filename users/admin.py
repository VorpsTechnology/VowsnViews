from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Address, Budget, Task, GuestList, Blog, Vendor


# class UserAdmin(UserAdmin):
#     list_display = ('email', 'user_full_name', 'date_joined', 'last_login', 'is_superuser', 'is_staff')
#     search_fields = ('email', 'user_full_name')
#     readonly_fields = ('date_joined', 'last_login')
#
#     filter_horizontal = ()
#     list_filter = ()
#     fieldsets = ()


# class AddressAdmin(admin.ModelAdmin):
#     list_display = [
#         'user',
#         'street_address',
#         'apartment_address',
#         'country',
#         'postal_code',
#         'address_type',
#         'default'
#     ]
#     list_filter = ['default', 'address_type', 'country']
#     search_fields = ['user', 'street_address', 'apartment_address', 'postal_code']


admin.site.register(User)  # , UserAdmin
admin.site.register(Address)
admin.site.register(Task)
admin.site.register(Budget)
admin.site.register(GuestList)
admin.site.register(Blog)
admin.site.register(Vendor)


