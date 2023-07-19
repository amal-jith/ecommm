from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import RegistrationForm, LoginForm
from .models import CustomUser


def register_login(request):
    if request.method == 'POST':
        # Registration form submitted
        registration_form = RegistrationForm(request.POST)
        login_form = LoginForm(request.POST)

        if registration_form.is_valid():
            # Process registration form
            username = registration_form.cleaned_data['username']
            password = registration_form.cleaned_data['password']
            full_name = registration_form.cleaned_data['full_name']
            # Create new user
            user = CustomUser.objects.create_user(username=username, password=password, full_name=full_name)
            # Log the user in
            login(request, user)
            return redirect('homepage:home')  # Redirect to home page after successful registration

    else:
        # Display registration and login forms
        registration_form = RegistrationForm()
        login_form = LoginForm()

    context = {
        'registration_form': registration_form,
        'login_form': login_form
    }

    return render(request, 'credentials/registration_login.html', context)


def user_logout(request):
    logout(request)
    return redirect('home')
