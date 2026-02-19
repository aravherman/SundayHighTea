from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class hightea(models.Model):
    sunday_date = models.DateField(unique=True)
    sponsor_name = models.CharField(max_length=200)
    contact = models.CharField(max_length=100, blank=True)
    status_choices = [
        ('Booked', 'Booked'),
        ('Available', 'Available'),
        ('Null', 'Null'),
    ]
    status = models.CharField(max_length=20, choices=status_choices, default='Available')
    payment = models.OneToOneField("Payment", on_delete=models.SET_NULL, null=True, blank=True)

    booked_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    booked_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sunday_date} - {self.sponsor_name}"
    
class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    sponsor_name = models.CharField(max_length=200, default="Unknown")
    contact = models.CharField(max_length=100, blank=True)
    sunday_date = models.DateField(null=True, blank=True)
    
    razorpay_order_id = models.CharField(max_length=100, unique=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=255, blank=True, null=True)

    amount = models.IntegerField()  # amount in paise
    currency = models.CharField(max_length=10, default="INR")

    status = models.CharField(max_length=50, default='Created')  # Created, Success, Failed
    verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.razorpay_order_id} - {self.status}"

