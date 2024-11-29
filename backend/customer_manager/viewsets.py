from rest_framework import viewsets, status

from rest_framework.response import Response
from customer_manager.models import Customer
from customer_manager.serializers import CustomerSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()
    permission_classes = ()

    def destroy(self, request, *args, **kwargs):
        customer = self.get_object()

        if customer.user:
            customer.user.delete()

        customer.delete()

        return Response(
            {"message": "Customer and associated user deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )
