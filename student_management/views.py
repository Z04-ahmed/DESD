from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.contrib import messages

from .forms import ProfileUpdateForm, UserUpdateForm
from .models import Profile  # Import Profile model

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                Profile.objects.create(user=user)  # Create an empty profile for the user
                messages.success(request, "Account successfully created. You can now log in.")
                return redirect('user_login')
            else:
                return render(request, 'signup.html', {'error': 'Username already exists'})
        else:
            return render(request, 'signup.html', {'error': 'Passwords do not match'})

    return render(request, 'signup.html')

def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        role = request.POST.get('role')  # Get the selected role from the dropdown


        # Authenticate using email
        user = authenticate(request, username=email, password=password)

        if user is not None:
                # Check if the user is staff and selected 'staff'
            if role == 'staff' and user.is_staff:
                auth_login(request, user)
                return redirect('staff_dashboard')  # Redirect to staff dashboard

            # Check if the user is a student and selected 'student'
            elif role == 'student' and not user.is_staff:
                auth_login(request, user)
                return redirect('dashboard')  # Redirect to student dashboard

            else:
                return render(request, 'login.html', {'error': 'Invalid role selected for this user.'})
        else:
            return render(request, 'login.html', {'error': 'Invalid email or password'})

    return render(request, 'login.html')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html', {'user': request.user})

def staff_dashboard(request):
    if not request.user.is_staff:
        return redirect('dashboard')  # If not staff, redirect to student dashboard
    
    return render(request, 'staff_dashboard.html', {'user': request.user})

def user_logout(request):
    auth_logout(request)
    return redirect('user_login')  # Redirect back to login page after logout


def edit_profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect('dashboard')

    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, 'edit_profile.html', {'user_form': user_form, 'profile_form': profile_form})

def index(request):
    return render(request, 'index.html')