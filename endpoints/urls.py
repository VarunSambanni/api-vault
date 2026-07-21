from django.urls import path
from . import views, admin

app_name = "endpoints"

urlpatterns = [
    path("", views.endpoint_list, name="endpoint-list"),
    path("new/", views.endpoint_create, name="endpoint-create"),
]