from django.db import models
from django.shortcuts import reverse
from django.utils import timezone
from django.db.models import Q
from ckeditor.fields import RichTextField

from users.models import User

LABEL_CHOICES = (
    ('Sale', 'Sale'),
    ('New Arrival', 'New Arrival'),
    ('Trending', 'Trending'),
    ('Top Selling', 'Top Selling'),
    ('Best Deals', 'Best Deals'),
    ('Recommendation', 'Recommendation'),
    ('Popular', 'Popular'),
)

REVIEW_RATING_CHOICES = (
    (1, 1),
    (1.5, 1.5),
    (2, 2),
    (2.5, 2.5),
    (3, 3),
    (3.5, 3.5),
    (4, 4),
    (4.5, 4.5),
    (5, 5),
)


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(default=timezone.now)
    # title = models.CharField(max_length=300)
    review_description = models.TextField()
    rating = models.FloatField(choices=REVIEW_RATING_CHOICES, max_length=3)

    def __str__(self):
        return f"{self.rating}_user"

    def get_absolute_url(self):  # Redirect to this link after adding review
        return reverse("product-list-view")

    def to_int(self):
        return int(self.rating)


class ParentCategory(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='parent_category', null=True, blank=True)  # image of slide ...
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):  # Redirect to this link after adding category , kwargs={'slug': self.slug })
        return reverse("admin-parent-category-list")


class CategoryQuerySet(models.QuerySet):
    def search(self, query=None):
        qs = self
        if query is not None:
            or_lookup = (Q(title__icontains=query) |
                         Q(description__icontains=query) |
                         Q(slug__icontains=query)
                         )
            qs = qs.filter(or_lookup).distinct()  # distinct() is often necessary with Q lookups
            return qs


class CategoryManager(models.Manager):
    def get_queryset(self):
        return CategoryQuerySet(self.model, using=self._db)

    def search(self, query=None):
        return self.get_queryset().search(query=query)


class Category(models.Model):
    parent_category = models.ForeignKey(ParentCategory, on_delete=models.CASCADE)

    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='category', null=True, blank=True)  # image of slide ...
    is_active = models.BooleanField(default=True)

    objects = CategoryManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):  # Redirect to this link after adding category , kwargs={'slug': self.slug })
        return reverse("admin-category-list")


class ProductQuerySet(models.QuerySet):
    def search(self, query=None):
        qs = self
        if query is not None:
            or_lookup = (Q(title__icontains=query) |
                         Q(description__icontains=query) |
                         Q(slug__icontains=query)
                         )
            qs = qs.filter(or_lookup).distinct()  # distinct() is often necessary with Q lookups
            return qs


class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def search(self, query=None):
        return self.get_queryset().search(query=query)



class Gender(models.Model):
    title = models.CharField(max_length=200, unique=True)
    image = models.ImageField(upload_to='category', null=True, blank=True)  # image of slide ...
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class ProductSize(models.Model):
    title = models.CharField(max_length=200, unique=True)  # image of slide ...
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class ProductColor(models.Model):
    title = models.CharField(max_length=200, unique=True)
    color_code = models.CharField(max_length=200, null=True, blank=True)# image of slide ...
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class ProductBrand(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='category', null=True, blank=True)  # image of slide ...
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class FunctionCategory(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='category', null=True, blank=True)  # image of slide ...
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title




class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    f_category = models.ForeignKey(FunctionCategory, on_delete=models.CASCADE, null=True, blank=True, help_text="Function category")
    brand = models.ForeignKey(ProductBrand, on_delete=models.CASCADE,  null=True, blank=True)
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE,  null=True, blank=True)
    # color = models.ForeignKey(ProductColor, on_delete=models.CASCADE,  null=True, blank=True)
    # size = models.ForeignKey(ProductSize, on_delete=models.CASCADE,  null=True, blank=True)

    title = models.CharField(max_length=200, unique=True)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    discount_price = models.DecimalField(max_digits=20, decimal_places=2)

    label = models.CharField(choices=LABEL_CHOICES, max_length=50, null=True, blank=True,
                             help_text="Item is of Sale, New Arrival etc or leave it blank for no label. \
                                        (Label will be displayed over a item.)")
    slug = models.SlugField(unique=True)

    stock_no = models.IntegerField(null=True, blank=True, help_text="Qty of stock!")  # number of products in stock
    # out_of_stock = models.BooleanField(default=False)

    short_description = RichTextField(help_text='To describe product in short', null=True, blank=True)
    description = RichTextField(help_text='Overview product', null=True, blank=True)

    vendor_name = models.CharField(max_length=200, null=True, blank=True)

    image_main = models.ImageField(upload_to='products', null=True, blank=True)
    image_2 = models.ImageField(upload_to='products', null=True, blank=True)
    image_3 = models.ImageField(upload_to='products', null=True, blank=True)
    image_4 = models.ImageField(upload_to='products', null=True, blank=True)
    image_5 = models.ImageField(upload_to='products', null=True, blank=True)
    image_6 = models.ImageField(upload_to='products', null=True, blank=True)
    image_7 = models.ImageField(upload_to='products', null=True, blank=True)
    image_8 = models.ImageField(upload_to='products', null=True, blank=True)
    image_9 = models.ImageField(upload_to='products', null=True, blank=True)
    image_10 = models.ImageField(upload_to='products', null=True, blank=True)
    
    
    image_main_link = models.URLField(null=True, blank=True)
    image_2_link = models.URLField(null=True, blank=True)
    image_3_link = models.URLField(null=True, blank=True)
    image_4_link = models.URLField(null=True, blank=True)
    image_5_link = models.URLField(null=True, blank=True)
    image_6_link = models.URLField(null=True, blank=True)
    image_7_link = models.URLField(null=True, blank=True)
    image_8_link = models.URLField(null=True, blank=True)
    image_9_link = models.URLField(null=True, blank=True)
    image_10_link = models.URLField(null=True, blank=True)
    
    video_1 = models.URLField(null=True, blank=True)
    video_2 = models.URLField(null=True, blank=True)
    video_3 = models.URLField(null=True, blank=True)
    video_4 = models.URLField(null=True, blank=True)
    video_5 = models.URLField(null=True, blank=True)
    video_6 = models.URLField(null=True, blank=True)
    video_7 = models.URLField(null=True, blank=True)
    video_8 = models.URLField(null=True, blank=True)
    video_9 = models.URLField(null=True, blank=True)
    video_10 = models.URLField(null=True, blank=True)
    
    review = models.ManyToManyField(Review, blank=True)

    is_active = models.BooleanField(default=True)
    trending = models.BooleanField(default=False)
    luxury_couture = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)

    objects = ProductManager()

    class Meta:
        db_table = 'products_product'
        ordering = ['title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):  # Redirect to this link after adding product
        return reverse("admin-product-list")

    def get_add_to_cart_url(self):  # Redirect to this link after adding product in cart
        return reverse("order-add-to-cart", kwargs={
            'slug': self.slug, 'buy_now': None
        })
    

    def get_search_redirect(self):
        return reverse("product-detail-view", kwargs={'pk': self.id})
        
    def get_image(self):
        if self.image_main:
            return self.image_main.url
        else:
            return self.image_main_link
            
    def discount_percentage(self):
         return int(100 - ((self.discount_price / self.price) * 100))

class VariationManger(models.Manager):
    def all(self):
        return super(VariationManger, self).all()

    def sizes(self):
        return self.all().filter(category='size')

    def colors(self):
        return self.all().filter(category='color')


VARIATION_CATEGORIES = (
    ('size', 'size'),
    ('color', 'color'),
)


class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_size = models.ForeignKey(ProductSize, on_delete=models.CASCADE, null=True, blank=True)
    
    category = models.CharField(choices=VARIATION_CATEGORIES, max_length=20, default='size')
    title = models.CharField(max_length=200)
    color_code = models.CharField(max_length=200, null=True, blank=True)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    discount_price = models.DecimalField(max_digits=20, decimal_places=2)
    # active = models.BooleanField(default=True)

    objects = VariationManger()

    class Meta:
        unique_together = ('title', 'product',)

    def __str__(self):
        return f'{self.product.title}_{self.title}_variation'

    def get_absolute_url(self):  # Redirect to this link after adding product
        return reverse("admin-product-detail", kwargs={'pk': self.product.id})


class Favorite(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # class Meta:
    #     unique_together = ('user', 'product',)

    def __str__(self):
        return f'{self.product.title}_{self.user}_favorite'




