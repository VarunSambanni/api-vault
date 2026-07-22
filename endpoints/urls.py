from django.urls import path
from . import views, admin

app_name = "endpoints"

urlpatterns = [
    path("", views.endpoint_list, name="endpoint-list"),
    path("new/", views.endpoint_create, name="endpoint-create"),
    path("<int:pk>/", views.endpoint_detail, name="endpoint-detail"),
path("<int:pk>/edit/", views.endpoint_update, name="endpoint-update")]