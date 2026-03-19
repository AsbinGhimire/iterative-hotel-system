from django.db import models
from django.core.exceptions import ValidationError
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.models import User

class Hotel(models.Model):
    STAR_RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]

    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    contact_info = models.CharField(max_length=15)
    total_rooms = models.PositiveIntegerField()
    star_rating = models.IntegerField(choices=STAR_RATING_CHOICES, default=3)
    manager = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hotels')
    image = models.ImageField(upload_to='hotels/', null=True, blank=True)

    def __str__(self):
        return self.name

class Room(models.Model):
    ROOM_TYPES = [
        ('Single', 'Single'),
        ('Double', 'Double'),
        ('Deluxe', 'Deluxe'),
    ]

    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='rooms')
    room_number = models.CharField(max_length=10)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES)
    price_per_night = models.DecimalField(max_digits=8, decimal_places=2)
    is_available = models.BooleanField(default=True)

    class Meta:
        unique_together = ('hotel', 'room_number')

    def clean(self):
        if self.price_per_night is not None and self.price_per_night <= 0:
            raise ValidationError({'price_per_night': "Price per night must be greater than zero."})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.hotel.name} - Room {self.room_number}"

class Customer(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.TextField()

    def __str__(self):
        return self.name

class Booking(models.Model):
    STATUS_CHOICES = [
        ('Booked', 'Booked'),
        ('Checked-In', 'Checked-In'),
        ('Checked-Out', 'Checked-Out'),
        ('Cancelled', 'Cancelled'),
    ]

    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='bookings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    customer = models.CharField(max_length=150)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Booked')

    def clean(self):
        if self.check_in and self.check_out:
            if self.check_in < timezone.now().date() and self._state.adding:
                raise ValidationError({'check_in': "Check-in date cannot be in the past."})

            if self.check_out <= self.check_in:
                raise ValidationError({'check_out': "Check-out date must be after check-in date."})

            if self.room:
                overlapping = Booking.objects.filter(
                    room=self.room,
                    check_in__lt=self.check_out,
                    check_out__gt=self.check_in
                ).exclude(id=self.id)

                if overlapping.exists():
                    raise ValidationError("This room is already booked for the selected dates.")

    def save(self, *args, **kwargs):
        self.full_clean()

        # Mark room as occupied or available based on status
        if self.status in ['Booked', 'Checked-In']:
            self.room.is_available = False
        elif self.status in ['Checked-Out', 'Cancelled']:
            self.room.is_available = True

        self.room.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.customer} - {self.room}"

class Payment(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(auto_now_add=True)
    payment_method = models.CharField(max_length=20)

    def save(self, *args, **kwargs):
        # Calculate amount based on stay duration and price
        nights = (self.booking.check_out - self.booking.check_in).days
        if nights < 1: nights = 1 # Minimum 1 night charge
        self.amount = nights * self.booking.room.price_per_night
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Payment for {self.booking}"


from django.db.models.signals import post_delete
from django.dispatch import receiver

@receiver(post_delete, sender=Booking)
def update_room_status_on_delete(sender, instance, **kwargs):
    """Ensure the room is marked as available when a booking is deleted."""
    room = instance.room
    # Check if there are any other active bookings for this room
    # For simplicity in this system, we mark it available.
    room.is_available = True
    room.save()
