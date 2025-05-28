from motopro.models import IfoodCustomer, IfoodOrder, IfoodItem
from django.utils import timezone

# Criar cliente
cliente = IfoodCustomer.objects.create(name="João Silva", phone="11999999999")

# Criar pedido
pedido = IfoodOrder.objects.create(
    event="ORDER_CREATED",
    order_id="abc123",
    created_at=timezone.now(),
    customer=cliente,
    total=35.00,
    status="RECEIVED"
)

# Criar itens
IfoodItem.objects.create(order=pedido, item_id="item1", name="Hamburguer Clássico", quantity=2, unit_price=15.00)
IfoodItem.objects.create(order=pedido, item_id="item2", name="Refrigerante", quantity=1, unit_price=5.00)
