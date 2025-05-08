from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from datetime import datetime
from .forms import CommunityForm
from .models import Community
from django.http import HttpResponseForbidden, HttpResponseNotAllowed, JsonResponse, HttpResponseBadRequest
import json
from .models import Event
from .models import Student
from django.urls import reverse
from django.db.models import Q
from .forms import EventForm
from django.core.exceptions import PermissionDenied
from django.utils import timezone
from .models import Community
from django.views.decorators.csrf import csrf_exempt
from .models import Announcement, Notification
from .forms import AnnouncementForm

from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import ProfileUpdateForm, UserUpdateForm
from .models import Profile  # Import Profile model

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        date_of_birth = request.POST['date_of_birth']

        if password == confirm_password:
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                # Convert date_of_birth string to a Python date object
                dob = datetime.strptime(date_of_birth, '%Y-%m-%d').date()
                Profile.objects.create(user=user, date_of_birth=dob)
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
    # Get all communities and announcements
    communities = Community.objects.all()
    announcements = Announcement.objects.order_by('-published_at')
    events = Event.objects.all()
    joined_event_ids = request.user.joined_events.values_list('id', flat=True)

    # Check if profile exists for the user
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile = None  # or handle this however you want (e.g., redirect to setup)

    # Handle announcement form
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save()

            # Send notifications to all users
            users = User.objects.exclude(id=request.user.id)  # Optional: Exclude the current user
            for user in users:
                Notification.objects.create(
                    user=user,
                    message=f"📢 New Announcement: {announcement.title}"
                )

            return redirect('dashboard')  # Replace with your actual dashboard URL name
    else:
        form = AnnouncementForm()

    # Fetch unread notifications for the user
    unread_notifications = request.user.notifications.filter(is_read=False)

    # Mark all unread notifications as read
    unread_notifications.update(is_read=True)

    # Render dashboard with the form, announcements, and unread notifications
    return render(request, 'dashboard.html', {
        'communities': communities,
        'profile': profile,
        'user': request.user,
        'announcements': announcements,
        'form': form,
        'unread_notifications': unread_notifications,
        'joined_event_ids': joined_event_ids,
        'events': events, # Pass unread notifications to the template
    })
    
@login_required
def staff_dashboard(request):
    students = User.objects.filter(is_staff=False, is_superuser=False)
    communities = Community.objects.all()
    announcements = Announcement.objects.all().order_by('-published_at')

    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.created_by = request.user
            announcement.save()

            # Create notifications for all students
            for student in students:
                Notification.objects.create(
                    user=student,
                    message=f"📢 {request.user.username} posted: {announcement.title}"
                )
            return redirect('staff_dashboard')  # or wherever you want
    else:
        form = AnnouncementForm()

    return render(request, 'staff_dashboard.html', {
        'students': students,
        'communities': communities,
        'form': form,
        'announcements': announcements,
    })

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


@login_required
@user_passes_test(lambda u: u.is_staff)  # Only staff can create
def create_community_api(request):
    if request.method == 'POST':
        try:
            raw_body = request.body.decode('utf-8')
            print("📦 Raw body:", raw_body)

            data = json.loads(raw_body)
            print("📋 Parsed data:", data)

            name = data.get('name')
            description = data.get('description')
            leader_id = data.get('leader_id')
            

            # Log to verify all fields
            print(f"Parsed fields: name={name}, desc={description}, leader_id={leader_id}, ")

            if not all([name, description, leader_id]):
                return HttpResponseBadRequest("Missing required fields")

            leader = User.objects.get(id=leader_id)

            community = Community.objects.create(
                name=name,
                description=description,
                leader=leader,
                created_by=request.user,
                
            )

            community.members.add(leader)
            community.save()

            return JsonResponse({
                'id': community.id,
                'name': community.name,
                'description': community.description,
                'leader_username': leader.username,
                
            })

        except Exception as e:
            print("❌ Error:", e)
            return HttpResponseBadRequest(str(e))

    return HttpResponseBadRequest("Invalid method")
@login_required
def edit_community(request, community_id):
    if not request.user.is_staff:
        return HttpResponseForbidden("You do not have permission to edit communities.")

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            community = Community.objects.get(id=community_id)

            community.name = data.get('name', community.name)
            community.description = data.get('description', community.description)

            leader_id = data.get('leader_id')
            if leader_id:
                from django.contrib.auth import get_user_model
                User = get_user_model()
                try:
                    new_leader = User.objects.get(id=leader_id)
                    community.leader = new_leader
                except User.DoesNotExist:
                    return JsonResponse({'status': 'error', 'message': 'Leader not found.'}, status=404)

            community.save()
            return JsonResponse({
                'status': 'success',
                'message': 'Community updated.',
                'new_leader_username': community.leader.username
            })
        except Community.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Community not found.'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON.'}, status=400)
    else:
        return HttpResponseNotAllowed(['POST'])
    
@login_required
def delete_community(request, community_id):
    if not request.user.is_staff:
        return HttpResponseForbidden("You do not have permission to delete communities.")

    if request.method == 'DELETE':
        try:
            community = Community.objects.get(id=community_id)
            community.delete()
            return JsonResponse({'status': 'success', 'message': 'Community deleted.'})
        except Community.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Community not found.'}, status=404)
    else:
        return HttpResponseNotAllowed(['DELETE'])
    
@login_required
def community_details(request, community_id):
    try:
        community = Community.objects.get(id=community_id)
        data = {
            'id': community.id,
            'name': community.name,
            'description': community.description,
            'leader_username': community.leader.username,
        }
        return JsonResponse(data)
    except Community.DoesNotExist:
        return JsonResponse({'error': 'Community not found'}, status=404)
    
@login_required
def notifications(request):
    user_notifications = request.user.notifications.order_by('-created_at')

    # Mark all unread notifications as read
    user_notifications.filter(is_read=False).update(is_read=True)

    return render(request, 'notifications.html', {'notifications': user_notifications})



@login_required
def event_list(request):
    events = Event.objects.all().order_by('-date')
    return render(request, 'events/event_list.html', {'events': events})

@login_required
def create_event(request):
        # ✅ Only allow community leaders
    # Check if user is a community leader OR staff
    is_community_leader = Community.objects.filter(leader=request.user).exists()
    
    if not (is_community_leader or request.user.is_staff):
        raise PermissionDenied("Only community leaders or staff can create events.")
    
        # Get communities where user is a leader
    user_communities = Community.objects.filter(leader=request.user)

    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()
            messages.success(request, "Event successfully created!")
            return redirect('event_list')
    else:
        initial_data = {'date': timezone.now()}
        form = EventForm(initial=initial_data)
        
                # Filter communities in the form
        if not request.user.is_staff:
            # If not staff, only show communities where user is a leader
            form.fields['community'].queryset = user_communities
        # Staff can see all communities

        return render(request, 'events/create_event.html', {
        'form': form,
        'user_communities': user_communities
    })

@login_required
def event_list(request):
    # Start with all events
    events = Event.objects.all().order_by('-date')

    # Get filter parameters
    query = request.GET.get('q', '')
    filter_type = request.GET.get('filter', '')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # Current date for filtering
    from django.utils import timezone
    now = timezone.now()

    # Apply text search filter
    if query:
        events = events.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(location__icontains=query)
        )

    # Apply upcoming/past events filter
    if filter_type == 'upcoming':
        events = events.filter(date__gte=now)
    elif filter_type == 'past':
        events = events.filter(date__lt=now)

    # Apply date range filter
    if start_date:
        try:
            start = timezone.datetime.strptime(start_date, '%Y-%m-%d').date()
            events = events.filter(date__date__gte=start)
        except ValueError:
            pass

    if end_date:
        try:
            end = timezone.datetime.strptime(end_date, '%Y-%m-%d').date()
            events = events.filter(date__date__lte=end)
        except ValueError:
            pass

    # Compute which events this student has joined
    joined_event_ids = []
    if not request.user.is_staff:
        try:
            student = Student.objects.get(email=request.user.email)
            joined_event_ids = list(student.events.values_list('id', flat=True))
        except Student.DoesNotExist:
            joined_event_ids = []

    context = {
        'events': events,
        'joined_event_ids': joined_event_ids,
        'query': query,
        'filter': filter_type,
        'start_date': start_date,
        'end_date': end_date,
    }

    return render(request, 'events/event_list.html', context)
@login_required
def delete_event(request, event_id):
    event = Event.objects.get(pk=event_id)

    # Check if the user is the organizer of the event
    if event.organizer != request.user:
        raise PermissionDenied("You don't have permission to delete this event.")

    if request.method == 'POST':
        event.delete()
        messages.success(request, "Event successfully deleted.")
        return redirect('event_list')

    return redirect('event_list')

@login_required
def get_event_details(request, event_id):
    try:
        event = Event.objects.get(id=event_id)

        # Ensure only the organizer can edit the event
        if event.organizer != request.user:
            return JsonResponse({'error': 'Not authorized'}, status=403)

        data = {
            'title': event.title,
            'description': event.description,
            'location': event.location,
            'date': event.date.isoformat(),
        }

        return JsonResponse(data)
    except Event.DoesNotExist:

        return JsonResponse({'redirect': True, 'url': reverse('event_list')})

@login_required
def edit_event(request, event_id):
    try:
        event = Event.objects.get(id=event_id)

        # Ensure only the organizer can edit the event
        if event.organizer != request.user:
            return JsonResponse({'success': False, 'message': 'Not authorized'}, status=403)

        if request.method == 'POST':
            # Update event with form data
            event.title = request.POST.get('title')
            event.description = request.POST.get('description')
            event.location = request.POST.get('location')
            event.date = request.POST.get('date')

            try:
                event.save()
                return JsonResponse({'success': True})
            except Exception as e:
                return JsonResponse({'success': False, 'message': str(e)})

        return JsonResponse({'success': False, 'message': 'Invalid request method'})
    except Event.DoesNotExist:
        # Instead of 404, return a JSON response indicating redirect
        return JsonResponse({'redirect': True, 'url': reverse('event_list')})



@login_required
def my_events(request):
    try:
        student = Student.objects.get(email=request.user.email)
        events = student.events.all()

        return render(request, 'events/my_events.html', {'events': events})

    except Student.DoesNotExist:
        messages.error(request, "Student profile not found.")
        return redirect('event_list')


@login_required
def join_event(request, event_id):
    if request.method == 'POST':
        event = get_object_or_404(Event, pk=event_id)

        # lookup student by email
        student, _ = Student.objects.get_or_create(
            email=request.user.email,
            defaults={'username': request.user.username}
        )

        if event in student.events.all():
            messages.info(request, "You’re already in that event.")
        else:
            student.events.add(event)
            messages.success(request, f"You have joined «{event.title}».")

    return redirect('event_list')


@login_required
def leave_event(request, event_id):
    if request.method == 'POST':
        event = get_object_or_404(Event, pk=event_id)
        try:
            student = Student.objects.get(email=request.user.email)
            if event in student.events.all():
                student.events.remove(event)
                messages.success(request, f"You have left «{event.title}».")
            else:
                messages.info(request, "You weren’t in that event.")
        except Student.DoesNotExist:
            messages.error(request, "Student profile not found.")
    return redirect('event_list')

def some_view(request):
    
    is_leader = Community.objects.filter(leader=request.user).exists()
    return render(request, 'events/create_event.html', {
        
        'is_leader': is_leader
    })
    


