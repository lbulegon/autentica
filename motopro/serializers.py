
# serializers.py

from rest_framework import serializers
from .models import TarefaConfig
from .models import IfoodWebhookEvent
class TarefaConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = TarefaConfig
        fields = ['id', 'nome', 'horario', 'ativa']

class IfoodWebhookEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = IfoodWebhookEvent
        fields = '__all__'




from rest_framework import serializers
from .models import Customer, DeliveryAddress, Order, Item

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['name', 'phone']

class DeliveryAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryAddress
        fields = ['street', 'number', 'complement', 'neighborhood', 'city', 'state', 'postal_code']

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['item_id', 'name', 'quantity', 'unit_price']

class OrderSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    delivery_address = DeliveryAddressSerializer()
    items = ItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['event', 'order_id', 'created_at', 'customer', 'delivery_address', 'total', 'status', 'items']

    def create(self, validated_data):
        customer_data = validated_data.pop('customer')
        delivery_data = validated_data.pop('delivery_address')
        items_data = validated_data.pop('items')

        customer, _ = Customer.objects.get_or_create(**customer_data)
        delivery_address = DeliveryAddress.objects.create(**delivery_data)
        order = Order.objects.create(customer=customer, delivery_address=delivery_address, **validated_data)

        for item_data in items_data:
            Item.objects.create(order=order, **item_data)

        return order
