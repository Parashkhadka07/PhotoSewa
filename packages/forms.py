from django import forms
from .models import Package

class PackageForm(forms.ModelForm):
    class Meta:
        model = Package
        exclude = ['photographer', 'active'] # We set these automatically in the view
        widgets = {
            'discount_end_date': forms.DateInput(attrs={'type': 'date', 'class': 'bg-white/5 border-white/10 text-white rounded-xl w-full p-3'}),
            'name': forms.TextInput(attrs={'placeholder': 'e.g., Wedding Elite', 'class': 'bg-white/5 border-white/10 text-white rounded-xl w-full p-3'}),
            'free_accessories': forms.Textarea(attrs={'rows': 3, 'class': 'bg-white/5 border-white/10 text-white rounded-xl w-full p-3'}),
        }