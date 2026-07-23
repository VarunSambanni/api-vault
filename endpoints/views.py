from django.shortcuts import render, redirect, get_object_or_404
from .forms import APIEndpointForm
from endpoints.models import APIEndpoint
from django.contrib.auth.decorators import login_required

@login_required
def endpoint_create(request):
    if request.method == "POST":
        form = APIEndpointForm(request.POST)
        if form.is_valid():
            endpoint = form.save(commit=False)
            endpoint.owner = request.user
            endpoint.save()
            form.save_m2m()
            return redirect("endpoints:endpoint-list")
    else:
        form = APIEndpointForm()

    return render(request,"endpoints/endpoint_form.html", {"form": form})

@login_required
def endpoint_list(request):
    endpoints = APIEndpoint.objects.filter(owner=request.user).select_related("category").prefetch_related("tags").order_by("-created_at")
    return render(request, "endpoints/endpoints_list.html", {"endpoints": endpoints})

@login_required
def endpoint_detail(request, pk):
    endpoints = (
        APIEndpoint.objects
        .filter(owner=request.user)
        .select_related("category")
        .prefetch_related("tags")
    )
    endpoint = get_object_or_404(endpoints, pk=pk)
    return render(request, "endpoints/endpoint_detail.html", {"endpoint": endpoint})

@login_required
def endpoint_delete(request, pk):
    endpoint = get_object_or_404(APIEndpoint, pk=pk, owner=request.user)
    if request.method == "POST":
        endpoint.delete()
        return redirect("endpoints:endpoint-list")

    context = {"endpoint": endpoint}

    return render(request, "endpoints/endpoint_confirm_delete.html", context)

@login_required
def endpoint_update(request, pk):
    endpoint = get_object_or_404(APIEndpoint, pk=pk, owner=request.user)

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



