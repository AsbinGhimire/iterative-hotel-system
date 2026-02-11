from django.contrib import admin
from .models import Room, Customer, Booking, Payment

admin.site.register(Room)
admin.site.register(Customer)
admin.site.register(Booking)
admin.site.register(Payment)
