from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .models import Room, Hotel, Booking, Profile
from .forms import BookingForm, ProfileUpdateForm, HotelForm, RoomForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User



def home(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            hotels = Hotel.objects.all()
            room_count = Room.objects.count()
            booking_count = Booking.objects.count()
        else:
            hotels = Hotel.objects.all()
            room_count = Room.objects.count()
            # We will show all hotels for regular users to book.
            booking_count = Booking.objects.filter(user=request.user).count() # simplistic link
            
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

def contact(request):
    return render(request, 'hotel/contact.html')

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
    form_class = HotelForm
    success_url = reverse_lazy('hotel_list')
    template_name = 'hotel/hotel_form.html'

    def form_valid(self, form):
        form.instance.manager = self.request.user
        return super().form_valid(form)

class HotelUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Hotel
    form_class = HotelForm
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

class HotelDetailView(DetailView):
    model = Hotel
    template_name = 'hotel/hotel_detail.html'
    context_object_name = 'hotel'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Convert amenities string to list
        if self.object.amenities:
            context['amenity_list'] = [a.strip() for a in self.object.amenities.split(',')]
        else:
            context['amenity_list'] = []
        return context


# Scoped Room Views
class RoomListView(LoginRequiredMixin, ListView):
    model = Room
    template_name = 'hotel/room_list.html'

    def get_queryset(self):
        return Room.objects.all()


class RoomCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Room
    form_class = RoomForm
    success_url = reverse_lazy('room_list')
    template_name = 'hotel/room_form.html'

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields['hotel'].queryset = Hotel.objects.all()
        return form


class RoomUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Room
    form_class = RoomForm
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
    context_object_name = 'bookings'

    def get_queryset(self):
        if self.request.user.is_staff:
            return Booking.objects.all().order_by('-id')
        return Booking.objects.filter(user=self.request.user).order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = self.get_queryset()
        context['stats'] = {
            'total': qs.count(),
            'active': qs.filter(status__in=['Booked', 'Checked-In']).count(),
            'completed': qs.filter(status='Checked-Out').count(),
            'cancelled': qs.filter(status='Cancelled').count(),
        }
        return context


class BookingCreateView(LoginRequiredMixin, CreateView):
    model = Booking
    form_class = BookingForm
    success_url = reverse_lazy('booking_list')
    template_name = 'hotel/booking_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class BookingUpdateView(LoginRequiredMixin, UpdateView):
    model = Booking
    form_class = BookingForm
    success_url = reverse_lazy('booking_list')
    template_name = 'hotel/booking_form.html'

    def get_queryset(self):
        if self.request.user.is_staff:
            return Booking.objects.all()
        return Booking.objects.filter(user=self.request.user)

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

def booking_bill(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')
    booking = get_object_or_404(Booking, pk=pk)
    if not request.user.is_staff and booking.user != request.user:
        return redirect('booking_list')
        
    nights = (booking.check_out - booking.check_in).days
    if nights < 1:
        nights = 1
    total_amount = nights * booking.room.price_per_night

    context = {
        'booking': booking,
        'nights': nights,
        'total_amount': total_amount,
    }
    return render(request, 'hotel/bill.html', context)

class ProfileView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'hotel/profile.html'
    context_object_name = 'profile'

    def get_object(self):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bookings'] = Booking.objects.filter(user=self.request.user).order_by('-check_in')
        return context

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileUpdateForm
    template_name = 'hotel/profile_form.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user.profile

class UserListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = User
    template_name = 'hotel/user_list.html'
    context_object_name = 'users'

class UserDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = User
    template_name = 'hotel/user_confirm_delete.html'
    success_url = reverse_lazy('user_list')
