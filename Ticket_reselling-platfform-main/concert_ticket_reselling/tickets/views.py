from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .models import Ticket, SellerProfile, AdminSettings
from .forms import TicketForm, SellerRegistrationForm
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic.edit import FormView

def home(request):
    tickets = Ticket.objects.all()
    admin_settings = AdminSettings.objects.first()  # Fetch admin settings (assuming only one entry)
    admin_whatsapp_number = admin_settings.admin_whatsapp_number if admin_settings else None
    
    search_query = request.GET.get('search', '')
    
    if search_query:
        # Use fuzzywuzzy to perform the search
        ticket_names = [ticket.event_name for ticket in tickets]
        
        # Extract top 10 matched ticket names based on fuzzy search
        matched_tickets = process.extract(search_query, ticket_names, limit=10)
        
        # Filter tickets based on the matched names with a minimum score threshold (e.g., 70)
        matched_ticket_names = [match[0] for match in matched_tickets if match[1] >= 70]
        
        # Filter tickets based on the matched names (case-insensitive)
        tickets = [ticket for ticket in tickets if ticket.event_name.lower() in [name.lower() for name in matched_ticket_names]]
    
    return render(request, 'tickets/home.html', {
        'tickets': tickets,
        'admin_whatsapp_number': admin_whatsapp_number,
        'search_query': search_query
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

# Seller Registration View
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

@login_required(login_url='seller_login')
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

# View for seller login
def seller_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('create_ticket')
    else:
        form = AuthenticationForm()
    return render(request, 'tickets/login.html', {'form': form})

def about(request):
    return render(request, 'tickets/about.html')


# Seller Registration View
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

@login_required(login_url='seller_login')
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

# View for seller login
def seller_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('create_ticket')
    else:
        form = AuthenticationForm()
    return render(request, 'tickets/login.html', {'form': form})

def about(request):
    return render(request, 'tickets/about.html')

class CustomPasswordResetView(SuccessMessageMixin, FormView):
    template_name = 'registration/password_reset.html'
    form_class = PasswordResetForm
    success_url = reverse_lazy('password_reset_done')
    success_message = "If the email exists, a reset link has been sent."

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            form.add_error('email', 'User with this email address is not registered. Please register first.')
            return self.form_invalid(form)
        return super().form_valid(form)