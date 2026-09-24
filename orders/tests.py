# orders/tasks.py

from celery import shared_task

from .models import Order


@shared_task
def send_order_confirmation(order_id):

    order = (
        Order.objects
        .select_related("user")
        .prefetch_related("items")
        .get(id=order_id)
    )

    print(
        f"Sending confirmation for Order #{order.id}"
    )

    # পরে এখানে email পাঠাবে