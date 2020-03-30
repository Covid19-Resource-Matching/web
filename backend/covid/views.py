from itertools import groupby

from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum, F, Q
from django.db import transaction

from .models import Supplier, Descriptor, Request, Supply


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

    # TODO: once fullfillment is in place, this query must be updated to only
    # show supplies not associated with a fulfillment
    user_supplies = request.user.supplier.supply_set.values("descriptor").annotate(
        quantity=Sum("quantity"), description=F("descriptor__description")
    )

    # The set of addable supplies is:
    # - Permanent descriptors
    # - Descriptors with unmet requests
    # Right now we just do 2 queries and deduplicate
    needed_supplies = Descriptor.objects.filter(
        Q(permanent=True) | Q(request__isnull=False)
    ).distinct()

    return render(
        request,
        "covid/supplier.html",
        context={"user_supplies": user_supplies, "needed_supplies": needed_supplies},
    )


@require_POST
@login_required
def update_supplies(request: HttpRequest) -> HttpResponse:
    # Add new supply rows for positive numbers. For negative numbers, the
    # recommended strategy is to remove unfulfilled supplies (by reducing their
    # counts) in oldest-first order.

    # The format here is ID => count

    # TODO: Validate IDs exist
    # TODO: Validate quantities
    # TODO: All validation should be done before any database writes
    # TODO: update_supplies should be a separate view from the "supplier"
    #       homepage

    with transaction.atomic():
        # TODO: Django supports bulk inserts with a single statement; use one
        # of those.
        for descriptor_id, quantity in request.POST.items():
            if descriptor_id == "csrfmiddlewaretoken":
                continue

            quantity = int(quantity)

            if quantity > 0:
                supply = Supply(
                    descriptor_id=descriptor_id,
                    supplier=request.user.supplier,
                    quantity=quantity,
                )
                supply.save()

    return redirect("supplier")
