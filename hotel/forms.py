from django import forms
from .models import Booking, Hotel, Room, Profile

class BookingForm(forms.ModelForm):
    """
    Form for creating and updating Bookings.
    Dynamically filters the 'hotel' and 'room' querysets based on the user's role:
    - Staff: See only hotels/rooms they manage.
    - Regular Users: See all hotels and only available rooms.
    """
    class Meta:
        model = Booking
        fields = ['customer', 'room', 'check_in', 'check_out', 'status', 'hotel']
        widgets = {
            'check_in': forms.DateInput(attrs={'type': 'date'}),
            'check_out': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            if user.is_staff:
                # Staff see their managed hotels and rooms
                self.fields['hotel'].queryset = Hotel.objects.filter(manager=user)
                self.fields['room'].queryset = Room.objects.filter(hotel__manager=user)
            else:
                # Customers see all hotels but only available rooms
                self.fields['hotel'].queryset = Hotel.objects.all()
                self.fields['room'].queryset = Room.objects.filter(is_available=True)

class ProfileUpdateForm(forms.ModelForm):
    """Form for users to update their profile settings (e.g., uploading a photo)."""
    class Meta:
        model = Profile
        fields = ['profile_photo']

class HotelForm(forms.ModelForm):
    """Form for administrators to create or edit Hotel entries."""
    class Meta:
        model = Hotel
        fields = ['name', 'location', 'contact_info', 'total_rooms', 'star_rating', 'image', 'description', 'amenities', 'website', 'email']

class RoomForm(forms.ModelForm):
    """Form for administrators to manage Room inventory and details."""
    class Meta:
        model = Room
        fields = ['room_number', 'room_type', 'price_per_night', 'is_available', 'hotel', 'description', 'size']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'size': forms.NumberInput(attrs={'placeholder': 'e.g. 25'}),
        }
