from datetime import datetime

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import get_template
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.core.mail import EmailMessage
from django.contrib import messages
from six import text_type

class AppTokenGenerator(PasswordResetTokenGenerator):

    def _make_hash_value(self, user, timestamp):
        return text_type(user.is_active) + text_type(user.pk) + text_type(timestamp)
        # if nt working try (text_type(user.is_active) + text_type(user.pk) + text_type(timestamp))


account_activation_token = AppTokenGenerator()


def send_activation_mail(request, message, user):
    current_site = get_current_site(request)
    email_body = {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    }

    link = reverse('activate', kwargs={'uidb64': email_body['uid'], 'token': email_body['token']})

    activate_url = 'https://' + current_site.domain + link

    email_subject = 'Welcome to '
    email_body_message = 'Please click the link and login to active your account'
    email_body = 'Hi ' + user.user_full_name + ', ' + email_body_message + '. \n\n <a href=' + activate_url + '>activate</a>'

    context = {}
    context['user_link'] = activate_url
    context['user_name'] = user.user_full_name
    context['date'] = datetime.now().date()
    message = get_template('home/email_template.html').render(context)
    email = EmailMessage(
        f'Activation mail',
        message,
        settings.AUTH_USER_MODEL,
        [user.email],
    )
    email.content_subtype = "html"
    email.send(fail_silently=False)
    # messages.success(request, message)
