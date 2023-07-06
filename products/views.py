from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic import View
from django.shortcuts import redirect, render
from django.contrib import messages

from products.filters import ProductFilter
from products.forms import ReviewForm
from products.models import (
    Product, Review, Favorite, ProductSize, ProductColor
)
from order.models import Cart
from products.models import Product, Category, FunctionCategory, ProductBrand
from listing.models import Listing, ListingLocation, ListingCategory


# Products
# Show all Products
class ProductListView(ListView):
    model = Product
    paginate_by = 50
    # Template name product_list.html
    # object_list variable name

    def get_queryset(self):
        queryset = self.model.objects.filter(is_active=True)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = Product.objects.filter(is_active=True)
        product_filter = ProductFilter(self.request.GET, queryset=query)

        if len(product_filter.qs) != len(query):
            context['object_list'] = product_filter.qs
            if len(product_filter.qs) < self.paginate_by:
                context['is_paginated'] = False

        context['size_filter'] = ProductSize.objects.filter(is_active=True)
        context['color_filter'] = ProductColor.objects.filter(is_active=True)
        context['label_list'] = ['Sale', 'Trending', 'Popular', 'Top Selling', 'Best Deal', 'New Arrival', 'Recommendation']

        context['filter'] = product_filter
        return context


class ProductDetailView(View):
    def get(self, *args, **kwargs):
        context = {}

        product = Product.objects.get(id=self.kwargs.get('pk'))
        if not product.is_active:
            return redirect('product-list-view')

        if self.request.user.is_authenticated:
            len_wishlist = Favorite.objects.filter(user=self.request.user).count()
            context['len_wishlist'] = len_wishlist

        price = product.price
        discount_price = product.discount_price

        try:
            review = product.review.filter(user=self.request.user)
            reviews = product.review.all()
            if reviews:
                review_rating_list = [float(review.rating) for review in reviews]  # list of review's rating
                review_rating_total = sum(review_rating_list)  # total of review rating
                average_review = review_rating_total / review.count()

                context['average_review'] = round(average_review * 2) / 2  # Round to nearest .5
                context['int_average_review'] = int(context['average_review'])  # Making it int
                context['reviews'] = reviews
            context['review_count'] = review.count()
            context['review_form'] = ReviewForm()
            context['reviewed'] = 'False'
            if review:
                context['reviewed'] = 'True'
            cart_query = Cart.objects.filter(user=self.request.user, ordered=True)
            context['purchased'] = "False"
            for cart in cart_query:
                if cart.product == product:
                    context['purchased'] = "True"
                    break
        except:
            pass
        context['object'] = product
        context['discount_percent'] = int(100 - ((discount_price / price) * 100))
        context['similar_product'] = Product.objects.filter(category=product.category)

        return render(self.request, 'products/product_detail.html', context)

    def post(self, *args, **kwargs):
        review_form = ReviewForm(self.request.POST)
        if review_form.is_valid():
            form = review_form.save(commit=False)
            form.user = self.request.user
            form.save()

            product = Product.objects.get(id=self.kwargs.get('pk'))
            product.review.add(form)
            product.save()
            messages.success(self.request, "Review Posted!")
        return redirect('product-detail-view', pk=self.kwargs.get('pk'))


# Show all Favorite
class FavoriteListView(LoginRequiredMixin, ListView):
    model = Favorite
    paginate_by = 10
    # queryset = Product.objects.filter(is_active=True)
    # Template name product_list.html
    # object_list variable name

    def get_queryset(self):
        queryset = Favorite.objects.filter(user=self.request.user)
        return queryset


class FavoriteAddView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        product = Product.objects.get(id=self.kwargs.get('pk'))
        fav_item = Favorite.objects.filter(user=self.request.user, product=product)
        if not fav_item:
            Favorite.objects.create(user=self.request.user, product=product)
            messages.success(self.request, "Product added to wishlist!")
            return redirect('product-detail-view', pk=product.id)
        messages.success(self.request, "Product already in wishlist!")
        return redirect('product-detail-view', pk=product.id)


class FavoriteRemoveView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        Favorite.objects.get(id=self.kwargs.get('pk')).delete()
        messages.success(self.request, "Product removed from wishlist!")
        return redirect('product-favorite-list')


# Review
# Add Review
class ReviewAddView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Review
    fields = ['title', 'review_description', 'rating']
    # template name review_form.html
    # TODO Pass form button and heading data
    # TODO add pytest_tests case

    def form_valid(self, form):
        review = form.instance
        review.user = self.request.user
        review.save()

        product = Product.objects.get(id=self.kwargs.get('pk'))
        product.review.add(review)
        product.save()
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_staff is True


# Update Review
class ReviewUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Review
    fields = ['title', 'review_description', 'rating']
    # template name review_form
    # TODO Pass form button and heading data

    def test_func(self):
        model = self.get_object()
        return self.request.user == model.user


# Delete Review
class ReviewDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Review
    fields = ['title', 'review_description', 'rating']
    success_url = '/'
    # template name review_confirm_delete.html
    # TODO display name in template and
    # TODO Pass form button and heading data

    def test_func(self):
        model = self.get_object()
        return self.request.user == model.user


class InHouseStore(View):
    def get(self, *args, **kwargs):
        list = Listing.objects.filter(is_in_house_listing=True, is_active = True)
        product = Product.objects.filter(label="Trending", is_active = True)
        vnv = Product.objects.filter(label="Vnv Best", is_active = True)
        recommendation = Product.objects.filter(label="Recommendation", is_active = True)
        product_luxury = ProductBrand.objects.filter(is_active = True)
        category = Category.objects.filter(is_active = True)
        f_category = FunctionCategory.objects.filter(is_active = True)
        return render(self.request, 'products/in_house_store.html', {'list_location': list, 'category': category, 'f_category': f_category, 'product': product,'product_luxury': product_luxury, 'vnv': vnv, 'recommendation': recommendation})
