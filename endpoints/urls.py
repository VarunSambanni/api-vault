from django.urls import path
from . import views, admin

app_name = "endpoints"

urlpatterns = [
    path("", views.endpoint_list, name="endpoint-list"),
    path("new/", views.endpoint_create, name="endpoint-create"),
    path("<int:pk>/edit/", views.endpoint_update, name="endpoint-update"),
    path("<int:pk>/delete/", views.endpoint_delete, name="endpoint-delete"),
    path("<int:pk>/", views.endpoint_detail, name="endpoint-detail"),
    path("organization/",views.organization_list,name="organization-list"),
    path("categories/new/", views.category_create, name="category-create"),
    path("tags/new/", views.tag_create, name="tag-create",),
]