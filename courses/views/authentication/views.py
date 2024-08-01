from django.http import request
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import View
from django.views.generic import FormView, TemplateView
from django.template.loader import render_to_string
from django.shortcuts import redirect, render
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from courses.forms import ContactMessageForm, RegisterForm, LoginForm, StudentForm
from courses.tokens import account_activation_token
from courses.models import User, Course, Teacher, Category, Student
from root.settings import DEFAULT_FROM_EMAIL


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'You have been logged out.')
        return redirect('index')


class LoginView(FormView):
    template_name = 'authentication/login.html'
    form_class = LoginForm
    success_url = '/index/'

    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(self.request, email=email, password=password)

        if user is not None:
            if Student.objects.filter(email=email).exists():
                user.is_student = True
                user.save()
            login(self.request, user)
            # messages.success(request, 'You are successfully logged in.')
            return super().form_valid(form)
        return super().form_invalid(form)


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
        user = None
        messages.error(request, 'Activation link is invalid!')

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        messages.success(request, 'Your account has been activated successfully! 😊')
        return redirect('index')
    else:
        return redirect('register')


def activate_email(request, user, to_email):
    subject = 'Activate your account'
    message = render_to_string('authentication/template_activate_account.html', {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.id)),
        'protocol': 'https' if request.is_secure() else 'http',
        'token': account_activation_token.make_token(user),
    })
    email = EmailMessage(subject, message, from_email=DEFAULT_FROM_EMAIL, to=[to_email, ])
    try:
        email.send()
        messages.success(request, 'Activation email has been sent. Please check your email.')
    except Exception as e:
        messages.error(request, f'Sorry, there was an error sending the activation email: {str(e)}')


class RegisterView(FormView):
    template_name = 'authentication/register.html'
    form_class = RegisterForm
    success_url = '/index/'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        activate_email(self.request, user, to_email=form.cleaned_data['email'])
        messages.success(self.request, 'Registration successful. Please check your email to activate your account.')
        return super().form_valid(form)


class ContactView(TemplateView):
    template_name = 'courses/contact.html'

    def get_context_data(self, **kwargs):
        form = ContactMessageForm()
        context = super().get_context_data(**kwargs)
        context['form'] = form
        return context

    def post(self, request, *args, **kwargs):
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you! Your message has been sent.')
            return redirect('contact')

        context = self.get_context_data(**kwargs)
        context['form'] = form
        return self.render_to_response(context)
