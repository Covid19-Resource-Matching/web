from enum import Enum

from django.db import models
from django.conf import settings


class Supplier(models.Model):
    user = settings.AUTH_USER_MODEL


# This is a temporary model for prototyping purposes
class Requester(models.Model):
    user = settings.AUTH_USER_MODEL


## A descriptor defines a particular kind of resource.
class Descriptor(models.Model):
    # TODO: make this searchable
    description = models.TextField()

    # If a descriptor is not permanent, it will be removed when there are no
    # requests or supplies of it, and it won't show up in auto-populated fields
    # if there are no unfulfilled supplies or requests
    permanent = models.BooleanField()


# The availability of a particular resource from a particular supplier in some quantity
class Supply(models.Model):
    descriptor = models.ForeignKey(Descriptor, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)


# A request of some quantity of a particular resource for a particular requester
class Request(models.Model):
    descriptor = models.ForeignKey(Descriptor, on_delete=models.CASCADE)
    requester = models.ForeignKey(Requester, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)


class FulfillmentState(Enum):
    Created = 0
    Assigned = 1
    Collected = 2
    Completed = 3


class Fulfillment(models.Model):
    supply: models.ForeignKey(Supply, on_delete=models.CASCADE)
    request: models.ForeignKey(Requester, on_delete=models.CASCADE)
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
