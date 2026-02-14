from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Room, Hotel, Booking
from .forms import BookingForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin



def home(request):
    return render(request, 'hotel/home.html')

# Hotel CRUD Views
class HotelListView(LoginRequiredMixin, ListView):
    model = Hotel
    template_name = 'hotel/hotel_list.html'
    
    def get_queryset(self):
        return Hotel.objects.filter(manager=self.request.user)

class HotelCreateView(LoginRequiredMixin, CreateView):
    model = Hotel
    fields = ['name', 'location', 'contact_info', 'total_rooms']
    success_url = reverse_lazy('hotel_list')
    template_name = 'hotel/hotel_form.html'

    def form_valid(self, form):
        form.instance.manager = self.request.user
        return super().form_valid(form)

class HotelUpdateView(LoginRequiredMixin, UpdateView):
    model = Hotel
    fields = ['name', 'location', 'contact_info', 'total_rooms']
    success_url = reverse_lazy('hotel_list')
    template_name = 'hotel/hotel_form.html'

    def get_queryset(self):
        return Hotel.objects.filter(manager=self.request.user)

class HotelDeleteView(LoginRequiredMixin, DeleteView):
    model = Hotel
    success_url = reverse_lazy('hotel_list')
    template_name = 'hotel/hotel_confirm_delete.html'

    def get_queryset(self):
        return Hotel.objects.filter(manager=self.request.user)


# Scoped Room Views
class RoomListView(LoginRequiredMixin, ListView):
    model = Room
    template_name = 'hotel/room_list.html'

    def get_queryset(self):
        return Room.objects.filter(hotel__manager=self.request.user)


class RoomCreateView(LoginRequiredMixin, CreateView):
    model = Room
    fields = ['room_number', 'room_type', 'price_per_night', 'is_available', 'hotel']
    success_url = reverse_lazy('room_list')
    template_name = 'hotel/room_form.html'

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields['hotel'].queryset = Hotel.objects.filter(manager=self.request.user)
        return form


class RoomUpdateView(LoginRequiredMixin, UpdateView):
    model = Room
    fields = ['room_number', 'room_type', 'price_per_night', 'is_available', 'hotel']
    success_url = reverse_lazy('room_list')
    template_name = 'hotel/room_form.html'

    def get_queryset(self):
        return Room.objects.filter(hotel__manager=self.request.user)

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields['hotel'].queryset = Hotel.objects.filter(manager=self.request.user)
        return form


class RoomDeleteView(LoginRequiredMixin, DeleteView):
    model = Room
    success_url = reverse_lazy('room_list')
    template_name = 'hotel/room_confirm_delete.html'

    def get_queryset(self):
        return Room.objects.filter(hotel__manager=self.request.user)


# Scoped Booking Views
class BookingListView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = 'hotel/booking_list.html'

    def get_queryset(self):
        return Booking.objects.filter(hotel__manager=self.request.user)


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
        return Booking.objects.filter(hotel__manager=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class BookingDeleteView(LoginRequiredMixin, DeleteView):
    model = Booking
    success_url = reverse_lazy('booking_list')
    template_name = 'hotel/booking_confirm_delete.html'

    def get_queryset(self):
        return Booking.objects.filter(hotel__manager=self.request.user)
