from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from student_management.models import Profile
from django import forms
from .models import Community
from .models import Announcement
from django.utils import timezone
from student_management.models import Event

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

        # Authenticate using email
        user = authenticate(request, username=email, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid email or password'})

    return render(request, 'login.html')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html', {'user': request.user})

def user_logout(request):
    auth_logout(request)
    return redirect('login')  # Redirect back to login page after logout

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'major', 'year', 'bio', 'achievements', 'campus_involvement', 'profile_picture']


class CommunityForm(forms.ModelForm):
    class Meta:
        model = Community
        fields = ['name', 'description', 'leader',]

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter announcement title'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter announcement content'
            }),
        }
class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'location', 'date','community']
        widgets = {
            'date': forms.DateTimeInput(attrs={
                'type': 'datetime-local', 
                'min': timezone.now().strftime('%Y-%m-%dT%H:%M')
            }),
                'community': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
        }
        
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['community'].empty_label = "Select a community"
        # Add help text to explain the community selection
        self.fields['community'].help_text = "Select the community this event belongs to"
        if user:
            self.fields['community'].queryset = Community.objects.filter(leader=user)
        else:
            self.fields['community'].queryset = Community.objects.none()
        
    def clean_date(self):
        date = self.cleaned_data.get('date')
        
        # Check if date is provided
        if not date:
            raise forms.ValidationError("Date is required.")
        
        # Get current time in the user's timezone
        now = timezone.now()
        
        # Allow events that start from now (inclusive)
        if date < now:
            raise forms.ValidationError("Event date must be in the present or future.")
        
        return date