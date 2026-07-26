from django.shortcuts import render, redirect, get_object_or_404
from .forms import APIEndpointForm, CategoryForm, TagForm
from endpoints.models import APIEndpoint
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import APIEndpoint, Category, Tag
from django.db.models import Q
from django.core.paginator import Paginator

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
    endpoints = APIEndpoint.objects.filter(owner=request.user).select_related("category").prefetch_related("tags")
    query = request.GET.get("q", "").strip()
    method = request.GET.get("method", "")
    category_value = request.GET.get("category", "")
    tag_value = request.GET.get("tag", "")
    favorite_only = request.GET.get("favorite") == "1"

    category_id = (int(category_value) if category_value.isdigit() else None)
    tag_id = (int(tag_value) if tag_value.isdigit() else None)

    if query:
        endpoints = endpoints.filter(Q(name__icontains=query) | Q(url__icontains=query) | Q(notes__icontains=query))

    if method in APIEndpoint.HTTPMethod.values:
        endpoints = endpoints.filter(method=method)

    if category_id is not None:
        endpoints = endpoints.filter(category__id=category_id)

    if tag_id is not None:
        endpoints = endpoints.filter(tags__id=tag_id)

    if favorite_only:
        endpoints = endpoints.filter(is_favorite=True)

    endpoints = endpoints.distinct().order_by("-created_at")

    paginator = Paginator(endpoints, 2)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "endpoints": page_obj,
        "page_obj": page_obj,
        "categories": Category.objects.filter(owner=request.user),
        "tags": Tag.objects.filter(owner=request.user),
        "method_choices": APIEndpoint.HTTPMethod.choices,
        "query": query,
        "selected_method": method,
        "selected_category_id": category_id,
        "selected_tag_id": tag_id,
        "favorite_only": favorite_only,
    }

    return render(request, "endpoints/endpoints_list.html", context)

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

@login_required
@require_POST
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk, owner=request.user)
    category.delete()
    return redirect("endpoints:organization-list")

@login_required
@require_POST
def tag_delete(request, pk):
    tag = get_object_or_404(Tag, pk=pk, owner=request.user)
    tag.delete()
    return redirect("endpoints:organization-list")

