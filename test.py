from domain.order import OrderOut, OrderInStock, OrderCancel,Order
import uuid
from domain import domain_logic as dl


def simulate_order_processing(order_id):
    items = []
    # Simulate order sending
    order = Order(order_id, items)
    print(f"Sending order: {order.to_json()}")
    dl.OrderSend(order)

    # Simulate checking order status
    order_status = dl.GetOrderStatus(order_id)
    print(f"Order status after sending: {order_status}")

    # Simulate out-of-stock event
    order_out = OrderOut(order_id)
    print(f"Simulating out-of-stock event: {order_out.to_json()}")
    dl.outstock(order_out)

    # Simulate checking order status after out-of-stock
    order_status = dl.GetOrderStatus(order_id)
    print(f"Order status after out-of-stock: {order_status}")

    # Simulate in-stock event
    order_in_stock = OrderInStock(order_id)
    print(f"Simulating in-stock event: {order_in_stock.to_json()}")
    dl.onstock(order_in_stock)

    # Simulate checking order status after in-stock
    order_status = dl.GetOrderStatus(order_id)
    print(f"Order status after in-stock: {order_status}")

    # Simulate order cancellation
    order_cancel = OrderCancel(order_id)
    print(f"Cancelling order: {order_cancel.to_json()}")
    dl.order_cancel(order_cancel)

    # Simulate checking order status after cancellation
    order_status = dl.GetOrderStatus(order_id)
    print(f"Order status after cancellation: {order_status}")



if __name__ == "__main__":
    # Generate a unique order ID
    order_id = str(uuid.uuid4())

    # Simulate the order processing workflow
    simulate_order_processing(order_id)
