from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("profile", views.profile, name="profile"),
    path("register_supplier", views.register_supplier, name="register_supplier"),
    path("supplier", views.supplier, name="supplier"),
    path("update_supplies", views.update_supplies, name="update_supplies"),
]
