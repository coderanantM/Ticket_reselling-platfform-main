from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .models import Ticket, SellerProfile, AdminSettings
from .forms import TicketForm, SellerRegistrationForm
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

class StatusFilterForm(forms.Form):
    status = forms.ChoiceField(choices=[('sold', 'Sold'), ('unsold', 'Unsold')], required=False)

def home(request):
    tickets = Ticket.objects.all()
    admin_settings = AdminSettings.objects.first()  # Fetch admin settings (assuming only one entry)
    admin_whatsapp_number = admin_settings.admin_whatsapp_number if admin_settings else None
    
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')

    if search_query:
        # Use fuzzywuzzy to perform the search
        ticket_names = [ticket.event_name for ticket in tickets]
        
        # Extract top 10 matched ticket names based on fuzzy search
        matched_tickets = process.extract(search_query, ticket_names, limit=10)
        
        # Filter tickets based on the matched names with a minimum score threshold (e.g., 70)
        matched_ticket_names = [match[0] for match in matched_tickets if match[1] >= 70]
        
        # Filter tickets based on the matched names (case-insensitive)
        tickets = [ticket for ticket in tickets if ticket.event_name.lower() in [name.lower() for name in matched_ticket_names]]
    
    if status_filter:
        tickets = tickets.filter(status=status_filter)

    status_filter_form = StatusFilterForm(initial={'status': status_filter})

    return render(request, 'tickets/home.html', {
        'tickets': tickets,
        'admin_whatsapp_number': admin_whatsapp_number,
        'search_query': search_query,
        'status_filter_form': status_filter_form,
    })

"""def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    admin_settings = AdminSettings.objects.first()  # Fetch admin settings (assuming only one entry)
    admin_whatsapp_number = admin_settings.admin_whatsapp_number if admin_settings else None

    return render(request, 'tickets/home.html', {
        'ticket': ticket,
        'admin_whatsapp_number': admin_whatsapp_number,
    })
"""

@login_required(login_url='login_and_redirect_to_tickets')
def update_ticket_status(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id, seller=request.user)
    if request.method == 'POST':
        status = request.POST.get('status')
        ticket.status = status
        ticket.save()
        messages.success(request, 'Ticket status updated successfully!')
    return redirect('home')

@login_required(login_url='login_and_redirect_to_tickets')
def delete_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id, seller=request.user)
    if request.method == 'POST':
        ticket.delete()
        messages.success(request, 'Ticket deleted successfully!')
    return redirect('my_tickets')

@login_required(login_url='login_and_redirect_to_tickets')
def my_tickets(request):
    user_tickets = Ticket.objects.filter(seller=request.user)
    return render(request, 'tickets/my_tickets.html', {'tickets': user_tickets})

def register_seller(request):
    if request.method == 'POST':
        form = SellerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            contact_info = form.cleaned_data['contact_info']
            SellerProfile.objects.create(user=user, contact_info=contact_info)
            login(request, user)
            messages.success(request, 'You have successfully registered!')
            return redirect('home')
    else:
        form = SellerRegistrationForm()
    return render(request, 'tickets/register_seller.html', {'form': form})

def login_and_redirect_to_create_ticket(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful!')
                return redirect('create_ticket')
    else:
        form = AuthenticationForm()
    return render(request, 'tickets/login_create_ticket.html', {'form': form})

def login_and_redirect_to_my_tickets(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful!')
                return redirect('my_tickets')
    else:
        form = AuthenticationForm()
    return render(request, 'tickets/login_my_tickets.html', {'form': form})

@login_required(login_url='login_and_redirect_to_create_ticket')
def create_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.seller = request.user
            ticket.save()
            messages.success(request, 'Ticket created successfully!')
            return redirect('home')
    else:
        form = TicketForm()
    return render(request, 'tickets/create_ticket.html', {'form': form})

def about(request):
    return render(request, 'tickets/about.html')


