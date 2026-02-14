import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hotel_management.settings')
django.setup()

from hotel.models import Room, Customer, Booking
from datetime import date, timedelta

def verify_sync():
    print("--- Starting Robust Room Status Sync Verification ---")
    
    unique_room_number = "SYNC-TEST-999"
    
    # 1. Cleanup any previous test data
    Booking.objects.filter(room__room_number=unique_room_number).delete()
    Room.objects.filter(room_number=unique_room_number).delete()

    # 2. Create a fresh room
    room = Room.objects.create(
        room_number=unique_room_number,
        room_type='Deluxe',
        price_per_night=150.0,
        is_available=True
    )
    print(f"Initial State: Room {room.room_number} is_available = {room.is_available}")

    # 3. Create a customer
    customer, _ = Customer.objects.get_or_create(name="Sync Tester", phone="9998887776")

    # 4. Create a booking
    print(f"\nCreating a booking for Room {unique_room_number}...")
    booking = Booking.objects.create(
        customer=customer,
        room=room,
        check_in=date.today(),
        check_out=date.today() + timedelta(days=2),
        status='Booked'
    )
    
    room.refresh_from_db()
    print(f"After Booking: Room is_available = {room.is_available}")
    if not room.is_available:
        print("✓ SUCCESS: Room marked as occupied automatically.")
    else:
        print("✗ FAILURE: Room status did not update.")

    # 5. Cancel the booking
    print("\nUpdating booking status to 'Cancelled'...")
    booking.status = 'Cancelled'
    booking.save()
    
    room.refresh_from_db()
    print(f"After Cancel: Room is_available = {room.is_available}")
    if room.is_available:
        print("✓ SUCCESS: Room marked as available after cancellation.")
    else:
        print("✗ FAILURE: Room status did not update.")

    # 6. Re-occupy (Check-In)
    print("\nRe-occupying room (status='Checked-In')...")
    booking.status = 'Checked-In'
    booking.save()
    room.refresh_from_db()
    print(f"After Check-In: Room is_available = {room.is_available}")

    # 7. Delete the booking
    print("\nDeleting the active booking...")
    booking.delete()
    
    room.refresh_from_db()
    print(f"After Deletion: Room is_available = {room.is_available}")
    if room.is_available:
        print("✓ SUCCESS: Room marked as available after deletion via signal.")
    else:
        print("✗ FAILURE: Room status did not update after deletion.")

    # Cleanup
    room.delete()
    print("\n--- Verification Complete ---")

if __name__ == "__main__":
    verify_sync()
