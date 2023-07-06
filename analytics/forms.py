from django import forms
from listing.models import DraftListing
from order.models import MiniOrder, ReturnMiniOrder, CancelMiniOrder
from .models import SendMail


class MiniOrderStatusForm(forms.ModelForm):
    class Meta:
        model = MiniOrder
        fields = ('order_status',)


class ReturnMiniOrderStatusForm(forms.ModelForm):
    class Meta:
        model = ReturnMiniOrder
        fields = ('return_status',)


class CancelMiniOrderStatusForm(forms.ModelForm):
    class Meta:
        model = CancelMiniOrder
        fields = ('cancel_status',)


class SendBulkMailForm(forms.ModelForm):
    class Meta:
        model = SendMail
        fields = ('title', 'body')


class ListingUpdateVendorsAssign(forms.ModelForm):
    class Meta:
        model = DraftListing
        fields = ['parent_category', 'category', 'location', 'sub_location', 'title', 'low_price', 'high_price',
                  'price_for', 'pre_low_price_text', 'post_low_price_text', 'pre_high_price_text',
                  'post_high_price_text',
                  'additional_text', 'meta_title', 'meta_description', 'short_description', 'description',
                  'more_info', 'catering_policy', 'decor_policy', 'alcohol_policy', 'dj_policy', 'video_1', 'video_2',
                  'video_3', 'video_4', 'video_5', 'video_6', 'video_7', 'video_8', 'video_9', 'video_10',
                  'image_main', 'image_2', 'image_3', 'image_4', 'image_5', 'image_main_link', 'image_2_link',
                  'image_3_link', 'image_4_link', 'image_5_link', 'is_active', 'is_verified', 'is_in_house_listing',
                  'address', 'trending', 'label']
