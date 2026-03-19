from django.contrib import admin
from .models import Room, Customer, Booking, Payment, Hotel

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'total_rooms', 'star_rating', 'manager')
    list_filter = ('star_rating', 'manager')
    search_fields = ('name', 'location')

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'hotel', 'room_type', 'price_per_night', 'is_available')
    list_filter = ('is_available', 'room_type', 'hotel')
    search_fields = ('room_number', 'hotel__name')

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone')
    search_fields = ('name', 'phone')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('customer', 'hotel', 'room', 'check_in', 'check_out', 'status')
    list_filter = ('status', 'hotel', 'check_in')
    search_fields = ('customer', 'room__room_number', 'hotel__name')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('booking', 'amount', 'payment_date', 'payment_method')
    list_filter = ('payment_date', 'payment_method')
    search_fields = ('booking__customer',)
