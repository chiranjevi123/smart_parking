from django.db import models
from django.contrib.auth.models import User
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile
from django.utils import timezone

# User Profile with Vehicle Details
class ParkingUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    vehicle_number = models.CharField(max_length=20)

    def __str__(self):
        return self.user.username


# Parking Area Model
class ParkingArea(models.Model):
    name = models.CharField(max_length=100)
    total_slots = models.IntegerField()
    price_per_slot = models.DecimalField(max_digits=6, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


# Individual Parking Slots
class ParkingSlot(models.Model):
    slot_number = models.CharField(max_length=10, unique=True)
    parking_area = models.ForeignKey(ParkingArea, on_delete=models.CASCADE)
    is_booked = models.BooleanField(default=False)  # This field exists

    def __str__(self):
        return f"Slot {self.slot_number} - {self.parking_area.name}"

# Booking Record (Stores Bookings & QR Code)
class ParkingRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slot = models.ForeignKey(ParkingSlot, on_delete=models.CASCADE)
    entry_time = models.DateTimeField(default=timezone.now) # Ensure this field is defined
    exit_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20)
    qr_code = models.ImageField(upload_to='qr_codes/', null=True, blank=True)

    def __str__(self):
        return f"Parking record for {self.user.username}"


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slot = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(
        max_length=20, choices=[('booked', 'Booked'), ('cancelled', 'Cancelled')]
    )

    def __str__(self):
        return f"{self.user.username} - {self.slot} ({self.start_time} to {self.end_time})"
