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


class MembershipApplication(models.Model):
    """Saves data from sadasya_form (अनलाइन सदस्यता)."""
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100)
    dob = models.DateField()
    email = models.EmailField()
    mobile = models.CharField(max_length=20)
    national_id_type = models.CharField(max_length=100)
    national_id_number = models.CharField(max_length=50)
    temporary_address = models.CharField(max_length=255, blank=True)
    mother_tongue = models.CharField(max_length=50)
    caste = models.CharField(max_length=50)
    pradesh = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    local_body_type = models.CharField(max_length=200)
    ward_number = models.PositiveSmallIntegerField()
    passport_photo = models.ImageField(upload_to='membership/passport/')
    citizenship_front = models.ImageField(upload_to='membership/citizenship/')
    citizenship_back = models.ImageField(upload_to='membership/citizenship/')
    payment_screenshot = models.ImageField(upload_to='membership/payment/')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Membership Application'
        verbose_name_plural = 'Membership Applications'

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"