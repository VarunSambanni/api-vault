from django import forms
from .models import APIEndpoint, Category, Tag
from django.core.exceptions import ValidationError

class APIEndpointForm(forms.ModelForm):
    class Meta:
        model = APIEndpoint
        fields = (
            "name",
            "method",
            "url",
            "category",
            "tags",
            "headers",
            "request_body",
            "sample_response",
            "notes",
            "is_favorite",
        )

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)

        if user is not None:
            self.fields["category"].queryset = Category.objects.filter(owner=user).order_by("name")

            self.fields["tags"].queryset = Tag.objects.filter(owner=user).order_by("name")

    def clean_headers(self):
        headers = self.cleaned_data.get("headers")

        if headers is None:
            return {}

        if not isinstance(headers, dict):
            raise ValidationError("Headers must be a JSON object containing name-value pairs")

        return headers

class APIEndpointAdminForm(APIEndpointForm):
    class Meta(APIEndpointForm.Meta):
        fields = ("owner",) + APIEndpointForm.Meta.fields
