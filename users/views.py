from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import (
    ObjectDoesNotExist, ValidationError
)
from django.contrib.auth.decorators import login_required
from django.core.validators import validate_email
from django.shortcuts import redirect, render
from django.utils.encoding import force_text
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic.edit import (
    FormView, CreateView, UpdateView, DeleteView
)
from django.views.generic.list import ListView
from django.utils.http import urlsafe_base64_decode
from django.http import JsonResponse

from .forms import (
    RegistrationForm, LoginForm, EmailForm, TaskAddForm, GuestAddForm,
    VendorRegistrationForm, BudgetAddForm,
)
from users.models import (
    User, Address, Task, Budget, GuestList, Blog, Vendor
)
from .utils import (
    account_activation_token, send_activation_mail
)
from listing.models import ListingFavorite, ParentListingCategory, ListingCategory


class SignUpView(SuccessMessageMixin, CreateView):
    template_name = 'users/register.html'
    success_url = '/'
    form_class = RegistrationForm

    # success_message = "Your account was created successfully"

    def form_valid(self, form):
        user = form.instance
        user.save()

        # Check if email is phone number or email (if email send mail)
        message = 'Account successfully created Please click the link in your mail and login to active your account.'
        send_activation_mail(self.request, message, user)

        messages.success(self.request,
                         "Your Account successfully created. Check your email inbox to activate your account.")
        return redirect('users-login')


# Vendor Registration View
class VendorSignUpView(View):
    context = {'parent_listing': ParentListingCategory.objects.all()}

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('vendor-home')
        self.context['user_form'] = RegistrationForm(prefix='UserForm')
        self.context['vendor_form'] = VendorRegistrationForm(prefix='VendorForm')

        return render(self.request, 'users/vendor_register.html', self.context)

    def post(self, *args, **kwargs):
        user_form = RegistrationForm(self.request.POST, prefix='UserForm')
        vendor_form = VendorRegistrationForm(
            self.request.POST, prefix='VendorForm')

        if user_form.is_valid() and vendor_form.is_valid():
            user = user_form.save()
            user.save()
            vendor = vendor_form.instance
            vendor.vendor_user = user
            user.is_vendor = True
            vendor.save()
            user.save()
            is_listing_on = self.request.POST.get('is_listing_on')
            if is_listing_on == 'on':
                vendor.is_listing_on = True
                vendor.save()
            messages.success(self.request, "Vendor Signed Up Successfully, Check your email inbox to activate your account.")
            message = 'Your account successfully created. Click on the link to activate your account. ' \
                      'your account. '
            send_activation_mail(self.request, message, user)
            
            return redirect('users-login')
        else:
            self.context['vendor_form'] = vendor_form
            self.context['user_form'] = user_form
            messages.warning(self.request, "Form not Valid")
            return render(self.request, 'users/vendor_register.html',
                          self.context)


def get_listing_category(request):
    id = request.GET.get('id')
    parent_listing_category = ParentListingCategory.objects.get(id=id)
    result = ListingCategory.objects.filter(
        parent_category=parent_listing_category)
    return render(request, 'users/listing_category.html', {'result': result})



def get_listing_category_landing(request):
    result_arr = []
    try:
        ids = [int(id) for id in request.GET.getlist('ids')]
        print('id is',ids)
        if ids:
            parent_listing_category = ParentListingCategory.objects.filter(id__in=ids)
            result = ListingCategory.objects.filter(parent_category__in=parent_listing_category)
            print(result)
            for item in result:
                sub_listing_info = {
                    'id': item.id,
                    'title': item.title,
                }
                result_arr.append(sub_listing_info)
    except Exception as e:
        pass
    return JsonResponse({
        'data':result_arr,
    })

# Login View


class LoginView(SuccessMessageMixin, FormView):
    form_class = LoginForm
    template_name = 'users/login.html'
    success_url = '/'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_vendor:
                return redirect('vendor-home')
            else:
                return redirect('user-account')
        else:
            return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # Validate data and show of user is active or inactive
        # TODO check if it is a good practise to redirect in form_valid function if not

        credentials = form.cleaned_data
        user = authenticate(email=credentials['email'],
                            password=credentials['password'])
        # Get the user
        try:
            user_query = User.objects.get(email=credentials['email'])
        except ObjectDoesNotExist:
            messages.error(
                self.request, 'Email or password is not correct')
            return redirect('users-login')

        # if user is not active show activation in HTML message!
        if user is not None:
            if user.is_active:
                login(self.request, user)
                vendor = Vendor.objects.filter(vendor_user= self.request.user).first()
                if vendor:
                    if vendor.is_listing_on:
                        return redirect('vendor-home')
                    if vendor.get_listing():
                        return redirect('vendor-home')
                    else:
                        return redirect('add-listing')
                return redirect('home')
        if not user_query.is_active:
            messages.warning(self.request, 'Your account is not active Please check your email inbox to your activate your account.')
            return redirect('users-login')
        else:
            messages.warning(self.request, 'Email or password not correct')
            return redirect('users-login')


# Verifying email on link click
class EmailVerificationView(View):
    def get(self, request, uidb64, token):
        try:
            pk = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=pk)

            if not account_activation_token.check_token(user, token):
                return redirect('users-login' + '?message=' + 'User already activated')

            if user.is_active:
                return redirect('users-login')
            user.is_active = True
            user.save()

            messages.success(request, 'Account activated successfully')
            return redirect('users-login')

        except Exception as ex:
            pass

        return redirect('users-login')


# TODO set a limit on verification sending
# Resend Mail or SMS for verification
class ResendMailConfirmationView(SuccessMessageMixin, FormView):
    form_class = EmailForm
    template_name = 'users/resend_conf.html'
    success_url = '/'

    def form_valid(self, form):
        # Validate email and send mail or SMS
        # TODO Send SMS

        # Get the user
        credentials = form.cleaned_data
        try:
            user = User.objects.get(email=credentials['email'])
        except ObjectDoesNotExist:
            messages.error(self.request, 'email is not correct')
            return redirect('users-resend-email-confirmation')

        # Check if user is active and send mail
        if not user.is_active:
            message = 'Verification Mail Resend!, Please click the link in your mail and login to active your account.'
            send_activation_mail(self.request, message, user)
            messages.info(
                self.request, 'Verification Mail Resend Successfully')
            return redirect('users-login')
        else:
            messages.info(
                self.request, 'User is already active. Please Login!')
            return redirect('users-login')


# User Update View
class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    fields = ['email', 'user_full_name', 'user_profile_pic', 'partner_full_name', 'wedding_date',
              'user_bride_groom', 'partner_bride_groom', 'wedding_venue', 'phone_number']

    # template_name = 'users/user_form_.html'

    # template name user_form
    def form_valid(self, form):
        credentials = form.cleaned_data
        phone = credentials['phone_number']

        if len(str(phone)) == 10:
            user = form.instance
            user.save()
            return redirect('profile')

    def test_func(self):
        model = self.get_object()
        return self.request.user == model


# Address
# Show all address
# TEST DONE
class AddressListView(LoginRequiredMixin, ListView):
    model = Address

    # Template name address_list.html
    # object_list variable name

    def get_queryset(self):
        queryset = Address.objects.filter(user=self.request.user)
        return queryset


# Add Address
# TEST DONE
class AddressAddView(LoginRequiredMixin, CreateView):
    model = Address
    fields = ['street_address', 'pin_code',
              'city', 'state', 'country', 'default']
    template_name = 'users/address_add.html'

    # template name address_form.html

    def form_valid(self, form):
        address = form.instance
        # address.save()
        if address.default:
            Address.objects.filter(
                default=True, user=self.request.user).update(default=False)
        if not address.default:
            add_count = Address.objects.filter(
                default=True, user=self.request.user).count()
            if add_count == 0:
                address.default = True
        address.save()
        self.request.user.address.add(address)
        return super().form_valid(form)


# Update Address
class AddressUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Address
    fields = ['street_address', 'pin_code',
              'city', 'state', 'country', 'default']

    # template name address_form

    def form_valid(self, form):
        address = form.instance
        # address.save()
        if address.default:
            Address.objects.filter(
                default=True, user=self.request.user).update(default=False)
        if not address.default:
            add_count = Address.objects.filter(
                default=True, user=self.request.user).count()
            if add_count == 0:
                address.default = True
        address.save()
        return super().form_valid(form)

    # checking if address if of current login in user or not
    def test_func(self):
        model = self.get_object()
        try:
            data = self.request.user.address.get(id=model.id)
            return True
        except:
            return False


# Delete Address
class AddressDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Address
    success_url = '/'

    # template name address_confirm_delete.html

    # checking if address if of current login in user or not
    def test_func(self):
        model = self.get_object()
        try:
            data = self.request.user.address.get(id=model.id)
            return True
        except:
            return False


class TaskView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        context = {}

        task_list = Task.objects.filter(user=request.user)
        task_form = TaskAddForm()
        context['task_list'] = task_list
        context['task_form'] = task_form

        return render(self.request, 'users/checklist_list.html', context)

    def post(self, request, *args, **kwargs):
        task_form = TaskAddForm(self.request.POST)
        if task_form.is_valid():
            task_form = task_form.save(commit=False)
            task_form.user = request.user
            task_form.save()
            messages.success(request, 'Task Added')
            return redirect('users-checklist')
        messages.warning(request, 'Invalid Form Data')
        return redirect('users-checklist')


@login_required()
def task_delete(request, pk):
    task = Task.objects.get(pk=pk)
    if task.user == request.user:
        task.delete()
        messages.warning(request, 'Task Delete')
        return redirect('users-checklist')
    messages.warning(request, 'Forbidden')
    return redirect('users-checklist')


class GuestView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        context = {}

        guest_list = GuestList.objects.filter(user=request.user)
        guest_form = GuestAddForm()
        context['guest_list'] = guest_list
        context['guest_form'] = guest_form

        return render(self.request, 'users/guest_list.html', context)

    def post(self, request, *args, **kwargs):
        guest_form = GuestAddForm(self.request.POST)
        if guest_form.is_valid():
            guest_form = guest_form.save(commit=False)
            guest_form.user = request.user
            guest_form.save()
            messages.success(request, 'Guest Added')
            return redirect('users-guest-list')

        messages.warning(request, 'Invalid Form Data')
        return redirect('users-guest-list')


@login_required()
def guest_delete(request, pk):
    guest = GuestList.objects.get(pk=pk)
    if guest.user == request.user:
        guest.delete()
        messages.warning(request, 'Guest Delete')
        return redirect('users-guest-list')
    messages.warning(request, 'Forbidden')
    return redirect('users-guest-list')


class BudgetView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        context = {}

        budget_list = Budget.objects.filter(user=request.user)
        budget_form = GuestAddForm()
        context['budget_list'] = budget_list
        context['budget_form'] = budget_form

        return render(self.request, 'users/budget_list.html', context)

    def post(self, request, *args, **kwargs):
        budget_form = BudgetAddForm(self.request.POST)
        if budget_form.is_valid():
            budget_form = budget_form.save(commit=False)
            budget_form.user = request.user
            budget_form.save()
            messages.success(request, 'Budget Update')
            return redirect('users-budget-list')

        messages.warning(request, 'Invalid Form Data')
        return redirect('users-budget-list')


@login_required()
def budget_delete(request, pk):
    budget = Budget.objects.get(pk=pk)
    if budget.user == request.user:
        budget.delete()
        messages.warning(request, 'Budget Delete')
        return redirect('users-budget-list')
    messages.warning(request, 'Forbidden')
    return redirect('users-budget-list')


class DashboardFavoriteListView(LoginRequiredMixin, ListView):
    model = ListingFavorite
    paginate_by = 10
    template_name = 'users/profile.html'

    # Template name listing_list.html
    # object_list variable name

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        budget_list = Budget.objects.filter(user=self.request.user)
        guest_list = GuestList.objects.filter(user=self.request.user)
        chectklist = Task.objects.filter(user=self.request.user).count
        context['budget_list'] = budget_list
        context['guest_list'] = guest_list
        context['checklist'] = chectklist
        return context

    def get_queryset(self):
        queryset = ListingFavorite.objects.filter(user=self.request.user)
        return queryset


class BlogListView(ListView):
    model = Blog

    # Template name blog_list.html
    # object_list variable name

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        vnv = Blog.objects.filter(is_vnv=True, is_active=True)
        context['vnv'] = vnv
        return context

    def get_queryset(self):
        queryset = self.model.objects.filter(is_active=True, is_vnv=False)
        return queryset


# Add Blog
class BlogAddView(LoginRequiredMixin, CreateView):
    model = Blog
    fields = ['title', 'image', 'short_description', 'description']

    # template name blog_form.html

    def form_valid(self, form):
        blog_object = form.instance
        blog_object.user = self.request.user
        blog_object.save()
        messages.success(self.request, 'Diarie Submitted Successfully. After Approval Your Diarie Listed Here.')
        return super().form_valid(form)


class BlogDetailView(View):
    def get(self, *args, **kwargs):
        context = {}

        product = Blog.objects.get(id=self.kwargs.get('pk'))
        context['object'] = product
        return render(self.request, 'users/blog_detail.html', context)