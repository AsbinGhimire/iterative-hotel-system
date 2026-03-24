from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .models import Room, Hotel, Booking, Profile
from .forms import BookingForm, ProfileUpdateForm, HotelForm, RoomForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User

def home(request):
    """
    Main landing page view.
    Displays dashboard statistics for authenticated users (Staff vs Regular).
    """
    if request.user.is_authenticated:
        if request.user.is_staff:
            hotels = Hotel.objects.all()
            room_count = Room.objects.count()
            booking_count = Booking.objects.count()
        else:
            hotels = Hotel.objects.all()
            room_count = Room.objects.count()
            booking_count = Booking.objects.filter(user=request.user).count()
            
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
    """Renders the static About Us page."""
    return render(request, 'hotel/about.html')

def contact(request):
    """Renders the static Contact Us page."""
    return render(request, 'hotel/contact.html')

class AdminRequiredMixin(UserPassesTestMixin):
    """Mixin to restrict view access to staff members only."""
    def test_func(self):
        return self.request.user.is_staff

# --- Hotel Management Views ---

class HotelListView(LoginRequiredMixin, ListView):
    """Displays a list of all hotels available in the system."""
    model = Hotel
    template_name = 'hotel/hotel_list.html'
    
    def get_queryset(self):
        return Hotel.objects.all()

class HotelCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    """Allows staff to add a new hotel. Automatically sets the manager to the current user."""
    model = Hotel
    form_class = HotelForm
    success_url = reverse_lazy('hotel_list')
    template_name = 'hotel/hotel_form.html'

    def form_valid(self, form):
        form.instance.manager = self.request.user
        return super().form_valid(form)

class HotelUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    """Allows staff to modify hotel details."""
    model = Hotel
    form_class = HotelForm
    success_url = reverse_lazy('hotel_list')
    template_name = 'hotel/hotel_form.html'

    def get_queryset(self):
        return Hotel.objects.all()

class HotelDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    """Allows staff to remove a hotel from the system."""
    model = Hotel
    success_url = reverse_lazy('hotel_list')
    template_name = 'hotel/hotel_confirm_delete.html'

    def get_queryset(self):
        return Hotel.objects.all()

class HotelDetailView(DetailView):
    """Displays detailed information about a specific hotel including amenities."""
    model = Hotel
    template_name = 'hotel/hotel_detail.html'
    context_object_name = 'hotel'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Convert the comma-separated amenities string into a list for template iteration
        if self.object.amenities:
            context['amenity_list'] = [a.strip() for a in self.object.amenities.split(',')]
        else:
            context['amenity_list'] = []
        return context


# --- Room Management Views ---

class RoomListView(LoginRequiredMixin, ListView):
    """Displays a list of all rooms across all hotels."""
    model = Room
    template_name = 'hotel/room_list.html'

    def get_queryset(self):
        return Room.objects.all()

class RoomCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    """Allows staff to create a new room and assign it to a hotel."""
    model = Room
    form_class = RoomForm
    success_url = reverse_lazy('room_list')
    template_name = 'hotel/room_form.html'

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields['hotel'].queryset = Hotel.objects.all()
        return form

class RoomUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    """Allows staff to update room specifications or availability."""
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
    """Allows staff to delete a room."""
    model = Room
    success_url = reverse_lazy('room_list')
    template_name = 'hotel/room_confirm_delete.html'

    def get_queryset(self):
        return Room.objects.all()


# --- Booking Management Views ---

class BookingListView(LoginRequiredMixin, ListView):
    """
    Displays bookings. 
    Staff see all bookings, while regular users see only their own.
    Includes booking statistics in context.
    """
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
    """Allows users to book a room. Passes the user object to the form for filtering available rooms."""
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
    """Allows users or staff to modify an existing booking."""
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
    """Allows staff to delete a booking record."""
    model = Booking
    success_url = reverse_lazy('booking_list')
    template_name = 'hotel/booking_confirm_delete.html'

    def get_queryset(self):
        return Booking.objects.all()

def update_booking_status(request, pk, status):
    """Quick action view for staff to change booking status (e.g., Check-In/Out)."""
    if not request.user.is_staff:
        return redirect('booking_list')
    booking = Booking.objects.get(pk=pk)
    if status in ['Booked', 'Checked-In', 'Checked-Out', 'Cancelled']:
        booking.status = status
        booking.save()
    return redirect('booking_list')

def booking_bill(request, pk):
    """Generates and displays a billing summary for a specific booking."""
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


# --- User Profile Views ---

class ProfileView(LoginRequiredMixin, DetailView):
    """Displays the user's profile information and their booking history."""
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
    """Allows users to update their profile information (loyalty points, photo)."""
    model = Profile
    form_class = ProfileUpdateForm
    template_name = 'hotel/profile_form.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user.profile

class UserListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    """Allows staff to view a list of all registered users."""
    model = User
    template_name = 'hotel/user_list.html'
    context_object_name = 'users'

class UserDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    """Allows staff to delete a user account."""
    model = User
    template_name = 'hotel/user_confirm_delete.html'
    success_url = reverse_lazy('user_list')
