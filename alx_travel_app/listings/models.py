from django.db import models
class Payment(models.Model):
    from django.db import models

class Payment(models.Model):
    # creating models for payment model 
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)  # Link to user
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100, unique=True)  # Unique transaction ID from Chapa
    currency = models.CharField(max_length=10, default='ETB')
    tx_ref = models.CharField(max_length=100, unique=True)  # Unique transaction reference
    payment_status = models.CharField(max_length=20, 
     default='pending'
             'Sucessful'
              'failed')  # e.g., pending, success, failed
    booking_reference = models.CharField(max_length=100, null=True, blank=True)  # Optional booking reference
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    chapa_response = models.JSONField(null=True, blank=True)  # Store Chapa API response

    def __str__(self):
        return f"{self.user} - {self.tx_ref} - {self.status}"

# Create your models here.
