from django import forms
from .models import Profile

class KycForm(forms.ModelForm):
    class Meta:
        model=Profile
        exclude=["user","created_at","specialization","profile_photo","kyc_verified","rejection_reason","permanent_address","Phone","price_charge","currency","no_of_cameras","location","intrest"]

class UpdateForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=["specialization","Phone","price_charge","currency","no_of_cameras","location"]
   
class UpdateFormClient(forms.ModelForm):
    class Meta:
        model=Profile
        fields=["Phone","location"]   