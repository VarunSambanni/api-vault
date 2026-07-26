from django.urls import path
from . import views

app_name = "endpoints"

urlpatterns = [
    path("", views.endpoint_list, name="endpoint-list"),
    path("new/", views.endpoint_create, name="endpoint-create"),
    path("organization/",views.organization_list,name="organization-list"),
    path("categories/new/", views.category_create, name="category-create"),
    path("categories/<int:pk>/delete/",views.category_delete,name="category-delete"),
    path("tags/new/", views.tag_create, name="tag-create",),
    path("tags/<int:pk>/delete/", views.tag_delete, name="tag-delete"),
    path("<int:pk>/edit/", views.endpoint_update, name="endpoint-update"),
    path("<int:pk>/delete/", views.endpoint_delete, name="endpoint-delete"),
    path("<int:pk>/try/", views.endpoint_try, name="endpoint-try"),
    path("<int:pk>/", views.endpoint_detail, name="endpoint-detail")
]