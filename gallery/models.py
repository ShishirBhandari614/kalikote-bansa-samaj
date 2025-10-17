from django.db import models

# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()  
    message = models.TextField()
    
    

    def __str__(self):
        return f"{self.name} - {self.message[:20]}..."
    

class Help_form(models.Model):
    full_name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    contact_number = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default="NPR")
    donation_purpose = models.TextField(blank=True, null=True)
    voucher_image = models.ImageField(upload_to='vouchers/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.amount} {self.currency}"
    

class Notices(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name