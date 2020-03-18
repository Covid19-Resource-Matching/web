from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from .models import Supplier


def index(request: HttpRequest) -> HttpResponse:
    return render(request, "covid/index.html", {})


@login_required
def profile(request: HttpRequest) -> HttpResponse:
    return render(request, "covid/profile.html", {})


# Register the currently authenticated user as a supplier
@require_POST
def register_supplier(request: HttpRequest) -> HttpResponse:
    if not request.user.is_authenticated:
        return HttpResponse(
            content="You must be logged in to register as a supplier", status=401,
        )

    Supplier.objects.get_or_create(user=request.user)
    return redirect("supplier")
