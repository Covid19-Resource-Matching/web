from django.contrib import admin

from .models import Descriptor, Supply, Request, Requester, Supplier, Fulfillment


@admin.register(Descriptor)
class DescriptorAdmin(admin.ModelAdmin):
    pass


@admin.register(Supply)
class SupplyAdmin(admin.ModelAdmin):
    pass


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    pass


@admin.register(Fulfillment)
class FulfillmentAdmin(admin.ModelAdmin):
    pass


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    pass


@admin.register(Requester)
class RequesterAdmin(admin.ModelAdmin):
    pass
