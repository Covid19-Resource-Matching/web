from django.urls import path

from . import views
from .views import SignUpView, ProfileView

urlpatterns = [
    path("", views.index, name="index"),
    path("profile", views.profile, name="profile"),
    path("register_supplier", views.register_supplier, name="register_supplier"),
    path("supplier", views.supplier, name="supplier"),
    path("update_supplies", views.update_supplies, name="update_supplies"),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('userprofile/<int:pk>/', ProfileView.as_view(), name='userprofile'),
    path('deleteuser', views.deleteuser, name='deleteuser'),
]
