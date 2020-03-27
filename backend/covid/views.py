from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum

from .models import Supplier, Descriptor


def index(request: HttpRequest) -> HttpResponse:
    return render(request, "covid/index.html", {})


@login_required
def profile(request: HttpRequest) -> HttpResponse:
    try:
        supplier = Supplier.objects.get(user=request.user)
    except Supplier.DoesNotExist:
        supplier = None

    return render(request, "covid/profile.html", context={"supplier": supplier})


# Register the currently authenticated user as a supplier
@require_POST
def register_supplier(request: HttpRequest) -> HttpResponse:
    if not request.user.is_authenticated:
        return HttpResponse(
            content="You must be logged in to register as a supplier", status=401,
        )

    Supplier.objects.get_or_create(user=request.user)
    return redirect("profile")


def user_is_supplier(user):
    return Supplier.objects.filter(user=user).exists()


@login_required
@user_passes_test(user_is_supplier, login_url="profile")
def supplier(request: HttpRequest) -> HttpResponse:
    return render(request, "covid/supplier.html")
