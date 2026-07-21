from django.contrib import admin
from .models import APIEndpoint

@admin.register(APIEndpoint)
class APIEndpointAdmin(admin.ModelAdmin):
    list_display = ('name', 'method', 'created_at', 'updated_at')
    list_filter = ('method', 'created_at')
    search_fields = ("name", "url", "notes")
    ordering = ('-created_at',)