
# services/pedido.py

from django.utils import timezone
from ..models import IfoodWebhookEvent, PedidoMotoboy, Motoboy

def atribuir_pedido_a_motoboy(pedido_id, motoboy_id):
    pedido = IfoodWebhookEvent.objects.get(id=pedido_id)
    motoboy = Motoboy.objects.get(id=motoboy_id)
    PedidoMotoboy.objects.create(
        motoboy=motoboy,
        pedido=pedido,
        assigned_at=timezone.now()
    )
    pedido.status = 'processed'
    pedido.save()

def atualizar_status_pedido(pedido_id, novo_status):
    pedido = IfoodWebhookEvent.objects.get(id=pedido_id)
    pedido.status = novo_status
    pedido.save()
    return f"Status do pedido {pedido_id} atualizado para {novo_status}"
