from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Product, Inventory, Dealer, Order, OrderItem
from .serializers import (
    ProductSerializer,
    InventorySerializer,
    DealerSerializer,
    OrderSerializer,
    OrderItemSerializer
)


# Product ViewSet
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


# Inventory ViewSet
class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer


# Dealer ViewSet
class DealerViewSet(viewsets.ModelViewSet):
    queryset = Dealer.objects.all()
    serializer_class = DealerSerializer


# Order ViewSet
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    # 🔒 Prevent update/delete after confirmation
    def update(self, request, *args, **kwargs):
        order = self.get_object()
        if order.status != 'draft':
            return Response(
                {"error": "Cannot edit confirmed order"},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        order = self.get_object()
        if order.status != 'draft':
            return Response(
                {"error": "Cannot delete confirmed order"},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().destroy(request, *args, **kwargs)

    # ✅ Confirm Order
    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        order = self.get_object()

        # Prevent re-confirm
        if order.status != 'draft':
            return Response(
                {"error": "Order already confirmed"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check and deduct stock
        for item in order.items.all():
            inventory = item.product.inventory

            if inventory.quantity < item.quantity:
                return Response(
                    {"error": f"Insufficient stock for {item.product.name}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Deduct stock
            inventory.quantity -= item.quantity
            inventory.save()

        # Update order status
        order.status = 'confirmed'
        order.save()

        return Response(
            {"message": "Order confirmed successfully"},
            status=status.HTTP_200_OK
        )


# OrderItem ViewSet (optional)
class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
