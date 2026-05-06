from django import forms
from .models import Profile

class KycForm(forms.ModelForm):
    class Meta:
        model=Profile
        exclude=["user","created_at","specialization","profile_photo","kyc_verified","rejection_reason","permanent_address"]

   