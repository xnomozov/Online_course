import logging

from django.contrib.auth import logout
from django.shortcuts import render
from django.contrib.admin import register
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import View
from django.views.generic import FormView
from django.template.loader import render_to_string
from django.shortcuts import redirect, get_object_or_404
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage

from courses.forms import EmailForm
from courses.tokens import account_activation_token
from courses.models import Course, User
from root.settings import EMAIL_HOST_USER

#
# def logout_page(request):
#     logout(request)
#     return render(request, 'courses/index.html')
#
#
# def activate(request, uidb64, token):
#     try:
#         uid = force_str(urlsafe_base64_decode(uidb64))
#         user = User.objects.get(pk=uid)
#     except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#         user = None
#
#     if user is not None and account_activation_token.check_token(user, token):
#         user.is_active = True
#         user.save()
#         login(request, user, backend='django.contrib.auth.backends.ModelBackend')
#         messages.success(request, 'Your account has been activated successfully!😊')
#         return redirect('customers')
#     else:
#         messages.error(request, 'Activation link is invalid!')
#         return redirect('register')
#
#
# def activate_email(request, user, to_email):
#     subject = 'Activate your account'
#     message = render_to_string('authentication/template_activate_account.html', {
#         'user': user.username,
#         'domain': get_current_site(request).domain,
#         'uid': urlsafe_base64_encode(force_bytes(user.id)),
#         'protocol': 'https' if request.is_secure() else 'http',
#         'token': account_activation_token.make_token(user),
#     })
#     email = EmailMessage(subject, message, to=[to_email])
#     try:
#         email.send()
#         messages.success(request,
#                          'Activation email has been sent. You have 5 minut to activate your account. '
#                          'Please check your email')
#     except Exception as e:
#         messages.error(request, f'Sorry, there was an error sending the activation email: {str(e)}')





class SendEmailView(View):
    def get(self, request):
        form = EmailForm()
        return render(request, 'courses/contact.html', {'form': form})

    def post(self, request):
        form = EmailForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            email_from = 'jm1495046@gmail.com'
            email_to = form.cleaned_data['email_from']
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, email_from, [email_to, ])
                messages.success(request, 'Message sent successfully.')
                return redirect('customers')
            except Exception as e:

                messages.error(request, 'Error sending message. Please try again later.')

        return render(request, 'courses/contact.html', {'form': form})
