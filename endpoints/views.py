from django.shortcuts import render, redirect
from django.http import HttpResponse

from .forms import APIEndpointForm
from .models import APIEndpoint

from endpoints.models import APIEndpoint

def endpoint_create(request):
    if request.method == "POST":
        form = APIEndpointForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("endpoints:endpoint-list")
    else:
        form = APIEndpointForm()

    context = {"form": form}

    return render(request,"endpoints/endpoint_form.html", context)

# Create your views here.
def endpoint_list(request):
    endpoints = APIEndpoint.objects.all().order_by('-created_at')
    context = {"endpoints": endpoints}

    return render(request, "endpoints/endpoints_list.html", context)
