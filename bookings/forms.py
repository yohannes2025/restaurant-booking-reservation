from django import forms
from .models import Booking
from django.forms.widgets import DateInput, TimeInput

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['full_name', 'email', 'phone', 'date', 'time', 'guests', 'special_request']
        widgets = {
            'date': DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'time': TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        }
        labels = {
            'guests': 'Number of Guests',
            'special_request': 'Special Requests (optional)',
        }
