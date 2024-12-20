import base64
import datetime
import os
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect

from userportal.forms import eventForm
from userportal.models import Event, Cart, Ticket


# Create your views here.
def index(request):
    event = Event.objects.all()
    return render(request, 'index.html', {'event': event})

def about(request):
    return render(request, 'about.html')


def registration(request):
    return render(request, 'registration.html')


def dashboard(request):
    if not request.user.is_staff:
        return redirect('index')


    total_events = Event.objects.count()
    upcoming_events_count = Event.objects.filter(status='upcoming').count()

    events = Event.objects.all()
    if request.method == 'POST':
        form = eventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = eventForm()
    users = User.objects.all()
    return render(request, 'adminstration.html', {'total_events': total_events,
    'upcoming_events_count': upcoming_events_count, 'form': form, 'events': events,'users': users})

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

def delete_event(request, id):
    event = get_object_or_404(Event, id=id)
    try:
        event.delete()
        messages.success(request, 'Your event has been deleted.')
    except Exception as e:
        messages.error(request, 'Your event could not be deleted.')
    return redirect('dashboard')

def events(request):
    events = Event.objects.all()
    return render(request, 'events.html', {'events': events})

def view_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    similar_events = Event.objects.filter(category=event.category).exclude(id=event.id)
    return render(request, 'view_event.html', {'event': event, 'similar_events': similar_events})

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        is_staff = request.POST.get('is_staff', '')

        if username and email and password:
            user = User.objects.create_user(username=username, email=email, password=password)
            if is_staff == 'on':
                user.is_staff = True
            user.save()
            messages.success(request, "Registration successful.")
            return redirect('login')
        else:
            messages.error(request, "All fields are required.")

    return render(request, 'registration.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "You are now logged in.")
                if user.is_staff:
                    return redirect('dashboard')
                else:
                    return redirect('index')
            else:
                messages.error(request, "Invalid email or password.")
        except User.DoesNotExist:
            messages.error(request, "User does not exist.")
    return redirect('registration')

def logout_view(request):
    logout(request)
    return redirect('index')

def delete_user(request, user_id):
    if request.method == 'POST':
        user = User.objects.get(id=user_id)
        if user.is_superuser:
            messages.error(request, "You can't delete superusers.")
        else:
            user.delete()
            messages.success(request, "User has been deleted.")
    return redirect('dashboard')

@login_required
def add_to_cart(request, id):
    event = get_object_or_404(Event, id=id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    ticket, created = Ticket.objects.get_or_create(event=event, user=request.user)
    if not created:
        ticket.quantity += 1
        ticket.save()
    else:
        cart.tickets.add(ticket)

    messages.success(request, 'Ticket added to cart.')
    return redirect('cart')

@login_required()
def cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    tickets = cart.tickets.all()

    subtotal = sum(ticket.quantity* Decimal(ticket.event.amount) for ticket in tickets)
    return render(request, 'cart.html', {'tickets': tickets, 'subtotal': subtotal})

@login_required()
def remove_from_cart(request, ticket_id):
    cart = get_object_or_404(Cart, user=request.user)
    ticket = get_object_or_404(Ticket, id=ticket_id)
    cart.tickets.remove(ticket)
    cart.save()
    messages.success(request, 'Ticket removed from cart.')
    return redirect('cart')

def my_tickets(request):
    return render(request, 'my_tickets.html')
