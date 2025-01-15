from django.contrib import admin
from .models import AdminSettings, SellerProfile, Ticket

# Register AdminSettings
@admin.register(AdminSettings)
class AdminSettingsAdmin(admin.ModelAdmin):
    list_display = ('admin_whatsapp_number',)

# Register SellerProfile
@admin.register(SellerProfile)
class SellerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'contact_info', 'whatsapp_number')  # Display user and phone numbers
    search_fields = ('user__username', 'contact_info', 'whatsapp_number')  # Allow searching by these fields

# Register Ticket with additional seller contact informations
@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('event_name', 'event_date', 'venue', 'price', 'seller', 'get_seller_contact')
    search_fields = ('event_name', 'venue', 'seller__username')

    def get_seller_contact(self, obj):
        """Fetch the seller's contact info from SellerProfile."""
        seller_profile = SellerProfile.objects.filter(user=obj.seller).first()
        return seller_profile.contact_info if seller_profile else "No contact info"

    get_seller_contact.short_description = 'Seller Contact'
