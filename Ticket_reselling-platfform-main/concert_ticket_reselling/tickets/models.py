from django.db import models
from django.contrib.auth.models import User

class Ticket(models.Model):
    event_name = models.CharField(max_length=255)
    event_date = models.DateField()
    venue = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    seller_name = models.CharField(max_length=255, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)  # New field
    category = models.CharField(max_length=50, null=True, blank=True)
    status = models.CharField(max_length=10, choices=[('sold', 'Sold'), ('unsold', 'Unsold')])
    
    def __str__(self):
        return f"{self.event_name} - {self.event_date} (Seller: {self.seller.username})"

class SellerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact_info = models.CharField(max_length=255)
    whatsapp_number = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return f"Profile of {self.user.username}"
    
class AdminSettings(models.Model):
    admin_whatsapp_number = models.CharField(max_length=15, blank=True, null=True)
    
    def __str__(self):
        return "Admin Settings"