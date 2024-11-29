from django.contrib.auth.models import User
from django.db import models


class Address(models.Model):
    """
    Model representing an address for users
    """

    address_line = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.address_line}, {self.city}"


class Customer(models.Model):
    """
    Model representing customer profile for an user in store
    """

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="customer_profile",
    )
    phone = models.CharField(max_length=20, blank=True, null=True)
    addresses = models.ManyToManyField(Address)

    def __str__(self) -> str:
        return self.user.get_full_name()
