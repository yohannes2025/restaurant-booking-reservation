# # bookings/forms.py
# from datetime import datetime, time
# from .models import Table, Booking
# from django import forms
# from django.utils import timezone
# from datetime import date, time, datetime, timedelta
# from django.contrib.auth.forms import UserCreationForm, UserChangeForm
# from django.contrib.auth.models import User
# from django import forms
# from datetime import date, time


# class CustomUserCreationForm(UserCreationForm):
#     class Meta(UserCreationForm.Meta):
#         model = User
#         # You can add 'email' here if you want it on your registration form.
#         # If adding email, consider making it unique in your User model if not already handled.
#         fields = UserCreationForm.Meta.fields + ('email',)


# class BookingForm(forms.ModelForm):
#     number_of_guests = forms.IntegerField(
#         min_value=1,
#         error_messages={'min_value': 'Number of guests must be at least 1.'}
#     )

#     class Meta:
#         model = Booking
#         fields = ['booking_date', 'booking_time', 'number_of_guests', 'notes']

#     def clean(self):
#         cleaned_data = super().clean()
#         booking_date = cleaned_data.get('booking_date')
#         booking_time = cleaned_data.get('booking_time')

#         if booking_date and booking_time:
#             booking_datetime = datetime.combine(booking_date, booking_time)
#             if booking_datetime < datetime.now():
#                 # Instead of raising a form-wide error, attach the error to 'booking_date' field
#                 self.add_error(
#                     'booking_date', "Booking date cannot be in the past.")

#         return cleaned_data

#     def clean_booking_time(self):
#         booking_time = self.cleaned_data.get('booking_time')
#         if booking_time and not time(9, 0) <= booking_time <= time(22, 0):
#             raise forms.ValidationError(
#                 "Booking time must be between 9:00 AM and 10:00 PM.")
#         return booking_time
        


# class AvailabilityForm(forms.Form):
#     check_date = forms.DateField(
#         label='Date',
#         widget=forms.DateInput(
#             attrs={'type': 'date', 'min': date.today().isoformat(), 'class': 'form-control'}),
#         initial=date.today()
#     )
#     check_time = forms.TimeField(
#         label='Time',
#         widget=forms.TimeInput(
#             attrs={'type': 'time', 'class': 'form-control'}),
#         initial=time(19, 0)  # Default to 7 PM
#     )
#     num_guests = forms.IntegerField(
#         label='Number of Guests',
#         min_value=1,
#         error_messages={'min_value': 'Number of guests must be at least 1.'},
#         widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
#         initial=2
#     )

#     def clean(self):
#         cleaned_data = super().clean()
#         check_date = cleaned_data.get('check_date')
#         check_time = cleaned_data.get('check_time')

#         if check_date and check_time:
#             # Combine naive datetime
#             check_datetime = datetime.combine(check_date, check_time)
#             # Make aware datetime with current timezone
#             check_datetime = timezone.make_aware(
#                 check_datetime, timezone.get_current_timezone())

#             if check_datetime < timezone.now() - timedelta(minutes=1):  # Allow current minute
#                 raise forms.ValidationError(
#                     "You cannot check availability for a past date and time.")

#             # Restaurant hours validation
#             if not (time(9, 0) <= check_time <= time(22, 0)):
#                 raise forms.ValidationError(
#                     "Restaurant is open from 9:00 AM to 10:00 PM.")

#         return cleaned_data


# class BookingStatusUpdateForm(forms.ModelForm):
#     class Meta:
#         model = Booking
#         fields = ['status', 'notes']  # Staff can update status and notes
#         widgets = {
#             'notes': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
#             'status': forms.Select(attrs={'class': 'form-select'}),
#         }
#         labels = {
#             'status': 'Booking Status',
#         }


# class TableForm(forms.ModelForm):
#     capacity = forms.IntegerField(
#         min_value=1,
#         error_messages={
#             'min_value': 'Ensure this value is greater than or equal to 1.'}
#     )

#     class Meta:
#         model = Table
#         fields = ['number', 'capacity']

#     def clean_number(self):
#         number = self.cleaned_data.get('number')
#         if Table.objects.filter(number=number).exists():
#             raise forms.ValidationError(
#                 "Table with this Table Number already exists.")
#         return number


# bookings/forms.py
from datetime import datetime, time
from .models import Table, Booking
from django import forms
from django.utils import timezone
from datetime import date, time, datetime, timedelta
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django import forms
from datetime import date, time


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        # You can add 'email' here if you want it on your registration form.
        # If adding email, consider making it unique in your User model if not already handled.
        fields = UserCreationForm.Meta.fields + ('email',)


class BookingForm(forms.ModelForm):
    number_of_guests = forms.IntegerField(
        min_value=1,
        error_messages={'min_value': 'Number of guests must be at least 1.'}
    )

    class Meta:
        model = Booking
        fields = ['booking_date', 'booking_time', 'number_of_guests', 'notes']
        widgets = {
            'booking_date': forms.DateInput(attrs={
                'type': 'text', # Change to text for Flatpickr, as it will initialize it
                'class': 'form-control flatpickr-date', # Add custom class for Flatpickr
                'placeholder': 'Select Date'
            }),
            'booking_time': forms.TimeInput(attrs={
                'type': 'text', # Change to text for Flatpickr
                'class': 'form-control flatpickr-time', # Add custom class for Flatpickr
                'placeholder': 'Select Time'
            }),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'number_of_guests': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        booking_date = cleaned_data.get('booking_date')
        booking_time = cleaned_data.get('booking_time')

        if booking_date and booking_time:
            booking_datetime = datetime.combine(booking_date, booking_time)
            # Make it timezone-aware for comparison with timezone.now()
            booking_datetime = timezone.make_aware(booking_datetime)

            if booking_datetime < timezone.now():
                self.add_error(
                    'booking_date', "Booking date cannot be in the past.")

        return cleaned_data

    def clean_booking_time(self):
        booking_time = self.cleaned_data.get('booking_time')
        if booking_time and not time(9, 0) <= booking_time <= time(22, 0):
            raise forms.ValidationError(
                "Booking time must be between 9:00 AM and 10:00 PM.")
        return booking_time


class AvailabilityForm(forms.Form):
    check_date = forms.DateField(
        label='Date',
        widget=forms.DateInput(
            attrs={'type': 'text', 'class': 'form-control flatpickr-date-check', 'placeholder': 'Select Date'}),
        initial=date.today()
    )
    check_time = forms.TimeField(
        label='Time',
        widget=forms.TimeInput(
            attrs={'type': 'text', 'class': 'form-control flatpickr-time-check', 'placeholder': 'Select Time'}),
        initial=time(19, 0)  # Default to 7 PM
    )
    num_guests = forms.IntegerField(
        label='Number of Guests',
        min_value=1,
        error_messages={'min_value': 'Number of guests must be at least 1.'},
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        initial=2
    )

    def clean(self):
        cleaned_data = super().clean()
        check_date = cleaned_data.get('check_date')
        check_time = cleaned_data.get('check_time')

        if check_date and check_time:
            # Combine naive datetime
            check_datetime = datetime.combine(check_date, check_time)
            # Make aware datetime with current timezone
            check_datetime = timezone.make_aware(
                check_datetime, timezone.get_current_timezone())

            if check_datetime < timezone.now() - timedelta(minutes=1):  # Allow current minute
                raise forms.ValidationError(
                    "You cannot check availability for a past date and time.")

            # Restaurant hours validation
            if not (time(9, 0) <= check_time <= time(22, 0)):
                raise forms.ValidationError(
                    "Restaurant is open from 9:00 AM to 10:00 PM.")

        return cleaned_data


class BookingStatusUpdateForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['status', 'notes']  # Staff can update status and notes
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'status': 'Booking Status',
        }


class TableForm(forms.ModelForm):
    capacity = forms.IntegerField(
        min_value=1,
        error_messages={
            'min_value': 'Ensure this value is greater than or equal to 1.'}
    )

    class Meta:
        model = Table
        fields = ['number', 'capacity']

    def clean_number(self):
        number = self.cleaned_data.get('number')
        if Table.objects.filter(number=number).exists():
            raise forms.ValidationError(
                "Table with this Table Number already exists.")
        return number