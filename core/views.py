from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login, logout

from .forms import SignUpForm, LoginForm

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