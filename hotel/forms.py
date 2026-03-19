from django import forms
from .models import Booking, Hotel, Room

class BookingForm(forms.ModelForm):
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
                self.fields['hotel'].queryset = Hotel.objects.filter(manager=user)
                self.fields['room'].queryset = Room.objects.filter(hotel__manager=user)
            else:
                self.fields['hotel'].queryset = Hotel.objects.all()
                self.fields['room'].queryset = Room.objects.filter(is_available=True)
