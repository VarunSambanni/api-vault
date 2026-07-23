from django.contrib import admin
from .models import APIEndpoint
from .forms import APIEndpointForm

@admin.register(APIEndpoint)
class APIEndpointAdmin(admin.ModelAdmin):
    form = APIEndpointForm
    list_display = (
        "name",
        "method",
        "is_favorite",
        "created_at",
        "updated_at",
    )
    list_filter = ("method", "is_favorite", "created_at")
    search_fields = ("name", "url", "notes")
    ordering = ("-created_at",)