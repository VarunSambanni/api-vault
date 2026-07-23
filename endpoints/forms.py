from django import forms
from .models import APIEndpoint
from django.core.exceptions import ValidationError

class APIEndpointForm(forms.ModelForm):
    class Meta:
        model = APIEndpoint
        fields = (
            "name",
            "method",
            "url",
            "headers",
            "request_body",
            "sample_response",
            "notes",
            "is_favorite",
        )

    def clean_headers(self):
        headers = self.cleaned_data.get("headers")

        if headers is None:
            return {}

        if not isinstance(headers, dict):
            raise ValidationError("Headers must be a JSON object containing name-value pairs")

        return headers

