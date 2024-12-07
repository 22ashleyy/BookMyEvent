import os
from lib2to3.fixes.fix_input import context

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from userportal.forms import eventForm
from userportal.models import Event


# Create your views here.
def index(request):
    event = Event.objects.all()
    return render(request, 'index.html', {'event': event})

def about(request):
    return render(request, 'about.html')

def registration(request):
    return render(request, 'registration.html')

def dashboard(request):
    total_events = Event.objects.count()
    upcoming_events_count = Event.objects.filter(status='upcoming').count()
    # recent_activity_count = User.objects.count()  # Placeholder for actual recent activity count

    events = Event.objects.all()
    if request.method == 'POST':
        form = eventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = eventForm()

    return render(request, 'adminstration.html', {'total_events': total_events,
    'upcoming_events_count': upcoming_events_count, 'form': form, 'events': events})

def edit_event(request, id):
    event = get_object_or_404(Event, id=id)
    if request.method == 'POST':
        form = eventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            if 'image' in request.FILES:
                messages.success(request, 'Your event and image have been updated.')
            else:
                messages.success(request, 'Your event has been updated.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Please correct the highlighted errors.')
    else:
        form = eventForm(instance=event)
    return render(request, 'adminstration.html', {'form': form, 'event': event})

def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    try:
        event.delete()
        messages.success(request, 'Event deleted successfully.')
    except Exception as e:
        messages.error(request, f'Error deleting event')
    return redirect('dashboard')

def events(request):
    events = Event.objects.all()
    return render(request, 'events.html', {'events': events})

def view_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'view_event.html', {'event': event})

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')

        if username and email and password:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            messages.success(request, "Registration successful.")
            return redirect('login')
        else:
            messages.error(request, "All fields are required.")

    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Invalid credentials.')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def my_tickets(request):
    # Add logic to fetch and display user's tickets
    return render(request, 'my_tickets.html')
@login_required
def cart(request):
    # Add logic to handle cart functionality
    return render(request, 'cart.html')