from django.contrib import admin
from .forms import APIEndpointAdminForm
from .models import APIEndpoint, Category, Tag

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ("name",)

@admin.register(APIEndpoint)
class APIEndpointAdmin(admin.ModelAdmin):
    form = APIEndpointAdminForm
    list_display = (
        "name",
        "owner",
        "method",
        "category",
        "is_favorite",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "method",
        "owner",
        "category",
        "tags",
        "is_favorite",
        "created_at",
    )
    search_fields = ("name", "url", "notes", "owner__username")
    filter_horizontal = ("tags",)
    ordering = ("-created_at",)