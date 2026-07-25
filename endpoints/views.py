from django.shortcuts import render, redirect, get_object_or_404
from .forms import APIEndpointForm, CategoryForm, TagForm
from endpoints.models import APIEndpoint
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import APIEndpoint, Category, Tag

@login_required
def endpoint_create(request):
    if request.method == "POST":
        form = APIEndpointForm(request.POST, user=request.user)
        if form.is_valid():
            endpoint = form.save(commit=False)
            endpoint.owner = request.user
            endpoint.save()
            form.save_m2m()
            return redirect("endpoints:endpoint-list")
    else:
        form = APIEndpointForm(user=request.user)

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
        form = APIEndpointForm(request.POST, instance=endpoint, user=request.user)

        if form.is_valid():
            updated_endpoint = form.save()

            return redirect(
                "endpoints:endpoint-detail",
                pk=updated_endpoint.pk,
            )
    else:
        form = APIEndpointForm(instance=endpoint, user=request.user)

    context = {"form": form, "endpoint": endpoint}

    return render(request, "endpoints/endpoint_form.html", context)

@login_required
def organization_list(request):
    return render(request, "endpoints/organization_list.html", organization_context(request.user))

def organization_context(user, category_form=None, tag_form=None):
    return {
        "categories": Category.objects.filter(owner=user),
        "tags": Tag.objects.filter(owner=user),
        "category_form": category_form or CategoryForm(user=user),
        "tag_form": tag_form or TagForm(user=user),
    }

@login_required
@require_POST
def category_create(request):
    form = CategoryForm(request.POST, user=request.user)

    if form.is_valid():
        category = form.save(commit=False)
        category.owner = request.user
        category.save()

        return redirect("endpoints:organization-list")

    context = organization_context(request.user, category_form=form)

    return render(request, "endpoints/organization_list.html",context,)

@login_required
@require_POST
def tag_create(request):
    form = TagForm(request.POST, user=request.user)

    if form.is_valid():
        tag = form.save(commit=False)
        tag.owner = request.user
        tag.save()

        return redirect("endpoints:organization-list")

    context = organization_context(request.user, tag_form=form)

    return render(request, "endpoints/organization_list.html",context,)

