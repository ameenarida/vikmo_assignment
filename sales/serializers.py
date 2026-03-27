from rest_framework import serializers
from .models import Product, Inventory, Dealer, Order, OrderItem


# Product Serializer
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


# Inventory Serializer
class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = '__all__'


# Dealer Serializer
class DealerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dealer
        fields = '__all__'


# OrderItem Serializer
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'unit_price', 'line_total']
        read_only_fields = ['unit_price', 'line_total']


# Order Serializer
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'dealer', 'status', 'order_number', 'total_amount', 'items']
        read_only_fields = ['status', 'order_number', 'total_amount']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order(**validated_data)
        order.save()

        total = 0

        for item in items_data:
            product = item['product']
            quantity = item['quantity']

            # Stock validation
            try:
                inventory = product.inventory
            except:
                raise serializers.ValidationError(
                    f"No inventory found for {product.name}"
                )

            if inventory.quantity < quantity:
                raise serializers.ValidationError(
                    f"Insufficient stock for {product.name}. Available: {inventory.quantity}"
                )

            unit_price = product.price
            line_total = quantity * unit_price

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                unit_price=unit_price,
                line_total=line_total
            )

            total += line_total

        order.total_amount = total
        order.save()

        return order