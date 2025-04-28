from django import forms
from .models import *

class ResortManagerForm(forms.ModelForm):
    class Meta:
        model = ResortManager
        fields = ['name', 'description', 'address', 'qr_code']  # Bao gồm trường qr_code
