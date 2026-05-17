from django import forms
from .models import Booking
from django.utils import timezone
from datetime import date,timedelta
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['phone', 'date_of_booking']
        widgets = {
            'date_of_booking': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone.isdigit():
            raise forms.ValidationError("Phone number must contain digits only.")
        if len(phone) != 10:
            raise forms.ValidationError("Phone number must be exactly 10 digits.")
        if not phone.startswith(('98', '97')):
            raise forms.ValidationError("Enter a valid Nepali phone number.")
        return phone

    def clean_date_of_booking(self):
        date = self.cleaned_data.get('date_of_booking')
        if date < timezone.now().date():
            raise forms.ValidationError("Booking date cannot be in the past.")
        return date
    
    def clean_date_of_booking(self):
        datee=self.cleaned_data.get("date_of_booking")
        today=date.today()
        gap=datee-today
        if not gap >= timedelta(2):
            raise forms.ValidationError("please book at lease 2 days before the event day!")
        return datee
  