from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request: HttpRequest) -> HttpResponse:
    return render(request, "covid/index.html", {})


@login_required
def profile(request: HttpRequest) -> HttpResponse:
    return render(request, "covid/profile.html", {})