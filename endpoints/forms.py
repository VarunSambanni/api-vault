from django import forms
from .models import APIEndpoint

class APIEndpointForm(forms.ModelForm):
    class Meta:
        model = APIEndpoint
        fields = ('name', 'method', 'url', 'notes')
