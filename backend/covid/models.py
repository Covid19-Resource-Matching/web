from enum import Enum

from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings


class Supplier(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


# This is a temporary model for prototyping purposes
class Requester(models.Model):
    # The user field has basic info for this person- name, email address
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # The *default* delivery address for this person. Used to populate new
    # fulfillments.
    # TODO: Consider using https://github.com/furious-luke/django-address.
    # This requires Google Maps API, which requires a billable Google Cloud
    # account, so we're punting it for now.
    address = models.TextField()

    phone_number = PhoneNumberField()

    def __str__(self):
        return self.user.username


# This is a temporary model for prototyping purposes
class Transporter(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    phone_number = PhoneNumberField()

    def __str__(self):
        return self.user.username


# This is a temporary model for prototyping purposes
class FulfillmentAdmin(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


## A descriptor defines a particular kind of resource.
class Descriptor(models.Model):
    # TODO: make this searchable
    description = models.TextField()

    # If a descriptor is not permanent, it will be removed when there are no
    # requests or supplies of it, and it won't show up in auto-populated fields
    # if there are no unfulfilled supplies or requests
    permanent = models.BooleanField()

    def __str__(self):
        return self.description


# The availability of a particular resource from a particular supplier in some quantity
class Supply(models.Model):
    descriptor = models.ForeignKey(Descriptor, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    measureWord = models.TextField()
    quantity = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"{self.supplier}: {self.quantity}× {self.descriptor}"


# A request of some quantity of a particular resource for a particular requester
class Request(models.Model):
    descriptor = models.ForeignKey(Descriptor, on_delete=models.CASCADE)
    # The person for whom this request should be delivered
    requester = models.ForeignKey(Requester, on_delete=models.CASCADE)

    # The person (if any) who entered this request
    request_admin = models.ForeignKey(
        FulfillmentAdmin, on_delete=models.SET_NULL, null=True
    )

    measureWord = models.TextField()
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.requester}: {self.quantity}× {self.descriptor}"


class FulfillmentState(Enum):
    Created = 0
    Assigned = 1
    Collected = 2
    Completed = 3


class Fulfillment(models.Model):
    supply = models.ForeignKey(Supply, on_delete=models.CASCADE)
    request = models.ForeignKey(Request, on_delete=models.CASCADE)
    measureWord = models.TextField()
    quantity = models.PositiveIntegerField()

    created = models.DateTimeField(auto_now_add=True)
    assigned = models.DateTimeField(null=True)
    collected = models.DateTimeField(null=True)
    completed = models.DateTimeField(null=True)

    @property
    def state(self) -> FulfillmentState:
        if self.assigned is None:
            return FulfillmentState.Created
        elif self.collected is None:
            return FulfillmentState.Assigned
        elif self.completed is None:
            return FulfillmentState.Collected
        else:
            return FulfillmentState.Completed

    # TODO: assignee
    # TODO: SQL constraint on relationships between timestamps
