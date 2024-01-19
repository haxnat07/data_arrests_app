from django.core.mail import send_mail

from django.contrib.auth.tokens import default_token_generator

from django.utils.encoding import force_bytes

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from django.contrib.auth import update_session_auth_hash

from django.shortcuts import get_object_or_404

from django.urls import reverse

from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login, logout

from .forms import *

from django.contrib import messages

# Create your views here.


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('dashboard')
        else:
            print(form.errors)
            # Check for non-password errors
            non_password_errors = any(field != 'password' for field in form.errors)
            if non_password_errors:
                messages.error(request, "Please complete all fields.")
            # Check for password-related errors
            if 'password' in form.errors:
                messages.error(request, "Password must contain 8 characters and should not be too common.")
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('dashboard')
            else:
                form.add_error(None, 'Invalid credentials')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


from django.conf import settings
# Reset password with email link
def custom_password_reset(request):
    if request.method == 'POST':
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            # Get the user instance associated with the provided email
            user = form.get_user(form.cleaned_data['email'])
            # Generate the token using the default_token_generator
            token = default_token_generator.make_token(user)

            # Save the form, triggering the sending of the password reset email
            form.save(
                domain_override=settings.CUSTOM_DOMAIN,
                request=request,
                from_email=None,
                email_template_name=None,
                subject_template_name=None,
                html_email_template_name=None,
                use_https=request.is_secure(),
                token_generator=default_token_generator, 
                extra_email_context=None,
            )
            
            print(f"uid: {user.id}, token: {token}")
            return render(request, 'forget_password/password_reset_done.html', {'uid': user.id, 'token': token})
    else:
        form = CustomPasswordResetForm()
    return render(request, 'forget_password/password_reset_form.html', {'form': form})


from django.contrib.auth import views as auth_views
from django.conf import settings
from django.urls import reverse_lazy


class CustomPasswordResetView(auth_views.PasswordResetView):
    template_name = 'forget_password/password_reset_form.html'
    email_template_name = 'forget_password/password_reset_email.html'
    subject_template_name = 'forget_password/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')
    extra_email_context = {'domain': settings.CUSTOM_DOMAIN, 'protocol': 'http'}
