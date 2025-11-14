from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, ProfileForm

# Register User
def register_user(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('login')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

# Login User
def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('dashboard')  # Redirect to dashboard after login
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid credentials.')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

# Logout User
def logout_user(request):
    logout(request)
    messages.info(request, 'You have successfully logged out.')
    return redirect('login')

# Profile Page (optional)
@login_required
def profile(request):
    return render(request, 'accounts/profile.html')

@login_required
def edit_profile(request):
    profile_obj = getattr(request.user, 'profile', None)
    if profile_obj is None:
        from .models import UserProfile
        profile_obj = UserProfile.objects.create(user=request.user, age=18, gender='P')

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile_obj)
        if form.is_valid():
            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            request.user.email = form.cleaned_data['email']
            request.user.save()
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')
    else:
        initial = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        }
        form = ProfileForm(instance=profile_obj, initial=initial)
    return render(request, 'accounts/profile_edit.html', {'form': form})

@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        logout(request)
        user.delete()
        messages.success(request, 'Your account has been deleted.')
        return redirect('home')
    return render(request, 'accounts/confirm_delete_account.html')
