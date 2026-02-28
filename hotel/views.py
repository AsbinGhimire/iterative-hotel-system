from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Room, Hotel, Booking
from .forms import BookingForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin



def home(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            hotels = Hotel.objects.all()
            room_count = Room.objects.count()
            booking_count = Booking.objects.count()
        else:
            hotels = Hotel.objects.all()
            room_count = Room.objects.count()
            booking_count = Booking.objects.filter(customer__phone=request.user.username).count() # Or filter by an actual linked profile if available. For now, we'll just count all bookings they can make. Let's fix user->customer link later, or just show their bookings if related. Actually, wait. The current system asks for Customer info in the booking form.
            # We will show all hotels for regular users to book.
            booking_count = Booking.objects.filter(customer__name=request.user.username).count() # simplistic link
            
        hotel_count = hotels.count()
        latest_hotels = hotels.order_by('-id')[:3]
        
        context = {
            'hotel_count': hotel_count,
            'room_count': room_count,
            'booking_count': booking_count,
            'latest_hotels': latest_hotels,
        }
    else:
        context = {}
    return render(request, 'hotel/home.html', context)

def about(request):
    return render(request, 'hotel/about.html')

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

# Hotel CRUD Views
class HotelListView(LoginRequiredMixin, ListView):
    model = Hotel
    template_name = 'hotel/hotel_list.html'
    
    def get_queryset(self):
        return Hotel.objects.all()

class HotelCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Hotel
    fields = ['name', 'location', 'contact_info', 'total_rooms', 'star_rating', 'image']
    success_url = reverse_lazy('hotel_list')
    template_name = 'hotel/hotel_form.html'

    def form_valid(self, form):
        form.instance.manager = self.request.user
        return super().form_valid(form)

class HotelUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Hotel
    fields = ['name', 'location', 'contact_info', 'total_rooms', 'star_rating', 'image']
    success_url = reverse_lazy('hotel_list')
    template_name = 'hotel/hotel_form.html'

    def get_queryset(self):
        return Hotel.objects.all()

class HotelDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Hotel
    success_url = reverse_lazy('hotel_list')
    template_name = 'hotel/hotel_confirm_delete.html'

    def get_queryset(self):
        return Hotel.objects.all()


# Scoped Room Views
class RoomListView(LoginRequiredMixin, ListView):
    model = Room
    template_name = 'hotel/room_list.html'

    def get_queryset(self):
        return Room.objects.all()


class RoomCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Room
    fields = ['room_number', 'room_type', 'price_per_night', 'is_available', 'hotel']
    success_url = reverse_lazy('room_list')
    template_name = 'hotel/room_form.html'

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields['hotel'].queryset = Hotel.objects.all()
        return form


class RoomUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Room
    fields = ['room_number', 'room_type', 'price_per_night', 'is_available', 'hotel']
    success_url = reverse_lazy('room_list')
    template_name = 'hotel/room_form.html'

    def get_queryset(self):
        return Room.objects.all()

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields['hotel'].queryset = Hotel.objects.all()
        return form


class RoomDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Room
    success_url = reverse_lazy('room_list')
    template_name = 'hotel/room_confirm_delete.html'

    def get_queryset(self):
        return Room.objects.all()


# Scoped Booking Views
class BookingListView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = 'hotel/booking_list.html'

    def get_queryset(self):
        if self.request.user.is_staff:
            return Booking.objects.all()
        # For simplicity currently, let's filter by customer name matching username.
        # Ideally, there is a one-to-one link from User to Customer.
        return Booking.objects.filter(customer__name=self.request.user.username)


class BookingCreateView(LoginRequiredMixin, CreateView):
    model = Booking
    form_class = BookingForm
    success_url = reverse_lazy('booking_list')
    template_name = 'hotel/booking_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class BookingUpdateView(LoginRequiredMixin, UpdateView):
    model = Booking
    form_class = BookingForm
    success_url = reverse_lazy('booking_list')
    template_name = 'hotel/booking_form.html'

    def get_queryset(self):
        if self.request.user.is_staff:
            return Booking.objects.all()
        return Booking.objects.filter(customer__name=self.request.user.username)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class BookingDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Booking
    success_url = reverse_lazy('booking_list')
    template_name = 'hotel/booking_confirm_delete.html'

    def get_queryset(self):
        return Booking.objects.all()

def update_booking_status(request, pk, status):
    if not request.user.is_staff:
        return redirect('booking_list')
    booking = Booking.objects.get(pk=pk)
    if status in ['Booked', 'Checked-In', 'Checked-Out', 'Cancelled']:
        booking.status = status
        booking.save()
    return redirect('booking_list')
