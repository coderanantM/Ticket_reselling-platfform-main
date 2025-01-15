from django import forms
from .models import Ticket
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms.widgets import DateInput

class SellerRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    contact_info = forms.CharField(max_length=255, required=True, help_text="Enter your contact info (e.g., WhatsApp number)")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'contact_info']

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['event_name', 'event_date', 'venue', 'price', 'seller_name', 'quantity', 'category']
        widgets = {
            'event_date': DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Adding custom label to category field
        self.fields['category'].label = "Category (VIP/Standing/etc)"
