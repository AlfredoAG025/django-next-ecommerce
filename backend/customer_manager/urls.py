from django.urls import include, path

from rest_framework import routers

from customer_manager.views import EmailConfirmationView
from customer_manager.viewsets import CustomerViewSet

router = routers.DefaultRouter()

router.register(r"customers", CustomerViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "confirm-email/<uidb64>/<token>/",
        EmailConfirmationView.as_view(),
        name="confirm-email",
    ),
]
