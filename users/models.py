# app_name/models.py
from django.contrib.auth.models import AbstractUser
from django.db.models import Model
from django.db.models.enums import TextChoices
from django.db.models.fields import CharField, EmailField
from django.db import models


class User(AbstractUser):
    class RoleType(TextChoices):
        ADMIN = "admin", "Admin"
        USER = "user", "User"
        SUPER_ADMIN = "super admin", "Super Admin"

    email = EmailField(unique=True)
    phone = CharField(max_length=13, unique=True)
    role = CharField(choices=RoleType, default=RoleType.USER, max_length=60)



#0-----------------------------------------parking-----------------------------


class ParkingZone(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    coordinates = models.CharField(max_length=100)  # Можно заменить на PointField (GeoDjango)
    total_spots = models.IntegerField()
    available_spots = models.IntegerField()
    hourly_rate = models.DecimalField(max_digits=6, decimal_places=2)
    daily_rate = models.DecimalField(max_digits=6, decimal_places=2)
    monthly_rate = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name


class ParkingSpot(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('occupied', 'Occupied'),
        ('reserved', 'Reserved'),
        ('maintenance', 'Maintenance'),
    ]

    SPOT_TYPE_CHOICES = [
        ('regular', 'Regular'),
        ('handicapped', 'Handicapped'),
        ('electric', 'Electric'),
    ]

    zone = models.ForeignKey(ParkingZone, on_delete=models.CASCADE, related_name='spots')
    spot_number = models.IntegerField(max_length=10)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='available')
    spot_type = models.CharField(max_length=12, choices=SPOT_TYPE_CHOICES, default='regular')

    def __str__(self):
        return f"{self.zone.name} - Spot {self.spot_number}"


class Reservation(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')
    spot = models.ForeignKey(ParkingSpot, on_delete=models.CASCADE, related_name='reservations')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    total_amount = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reservation {self.id} by {self.user.username}"

#------------------------------------------------------payment


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('card', 'Card'),
        ('cash', 'Cash'),
        ('paypal', 'Paypal'),
        # и другие методы
    ]

    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name='payments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES)
    status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES)
    transaction_id = models.IntegerField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.transaction_id} - {self.status}"
