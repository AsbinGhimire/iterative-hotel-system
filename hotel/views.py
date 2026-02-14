from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Room
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin



def home(request):
    return render(request, 'hotel/home.html')

class RoomListView(LoginRequiredMixin, ListView):
    model = Room
    template_name = 'hotel/room_list.html'


class RoomCreateView(LoginRequiredMixin, CreateView):
    model = Room
    fields = '__all__'
    success_url = reverse_lazy('room_list')
    template_name = 'hotel/room_form.html'


class RoomUpdateView(LoginRequiredMixin, UpdateView):
    model = Room
    fields = '__all__'
    success_url = reverse_lazy('room_list')
    template_name = 'hotel/room_form.html'


class RoomDeleteView(LoginRequiredMixin, DeleteView):
    model = Room
    success_url = reverse_lazy('room_list')
    template_name = 'hotel/room_confirm_delete.html'


from .models import Booking

class BookingListView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = 'hotel/booking_list.html'


class BookingCreateView(LoginRequiredMixin, CreateView):
    model = Booking
    fields = '__all__'
    success_url = reverse_lazy('booking_list')
    template_name = 'hotel/booking_form.html'


class BookingUpdateView(LoginRequiredMixin, UpdateView):
    model = Booking
    fields = '__all__'
    success_url = reverse_lazy('booking_list')
    template_name = 'hotel/booking_form.html'


class BookingDeleteView(LoginRequiredMixin, DeleteView):
    model = Booking
    success_url = reverse_lazy('booking_list')
    template_name = 'hotel/booking_confirm_delete.html'
