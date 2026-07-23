from django.shortcuts import render, redirect, get_object_or_404
from .forms import APIEndpointForm
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

def endpoint_list(request):
    endpoints = APIEndpoint.objects.all().order_by('-created_at')
    context = {"endpoints": endpoints}

    return render(request, "endpoints/endpoints_list.html", context)

def endpoint_detail(request, pk):
    endpoint = get_object_or_404(APIEndpoint, pk=pk)
    context = {"endpoint": endpoint}

    return render(request, "endpoints/endpoint_detail.html", context)

def endpoint_delete(request, pk):
        endpoint = get_object_or_404(APIEndpoint, pk=pk)
        if request.method == "POST":
            endpoint.delete()
            return redirect("endpoints:endpoint-list")

        context = {"endpoint": endpoint}

        return render(request, "endpoints/endpoint_confirm_delete.html", context)

def endpoint_update(request, pk):
    endpoint = get_object_or_404(APIEndpoint, pk=pk)

    if request.method == "POST":
        form = APIEndpointForm(request.POST, instance=endpoint)

        if form.is_valid():
            updated_endpoint = form.save()

            return redirect(
                "endpoints:endpoint-detail",
                pk=updated_endpoint.pk,
            )
    else:
        form = APIEndpointForm(instance=endpoint)

    context = {"form": form, "endpoint": endpoint}

    return render(request, "endpoints/endpoint_form.html", context)



