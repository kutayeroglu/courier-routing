import random

from helpers import manhattan_distance
from order import Order

def assign_order_to_courier(order_list, courier):
    """
    Assigns the nearest unassigned order to a courier if available.

    Parameters:
    - order_list (list): List of Order objects.
    - courier (Courier): The courier to assign an order to.

    Returns:
    - None
    """
    if not courier.is_busy:
        # Find the nearest unassigned order
        unassigned_orders = [order for order in order_list if not order.assigned]
        if unassigned_orders:
            # Sort orders by Manhattan distance
            unassigned_orders.sort(key=lambda o: manhattan_distance(courier.location, o.origin))
            nearest_order = unassigned_orders[0]
            courier.current_order = nearest_order
            nearest_order.assigned = True
            courier.is_busy = True
            nearest_order.status = 'assigned'
            print(f"Courier at {courier.location} assigned to order {nearest_order.origin} -> {nearest_order.destination}")


def handle_rejected_order(order, order_list):
    """
    Handles the rejection of an order by a courier.

    Parameters:
    - order (Order): The order being rejected.
    - order_list (list): The list of Order objects in the system.

    Returns:
    - None
    """
    order.patience -= 1  # Decrement patience
    if order.patience > 0:
        order.assigned = False
        order.status = 'pending'
        order_list.append(order)  # Reassign
        print(f"Order {order.origin} -> {order.destination} is back in the queue with patience {order.patience}.")
    else:
        order.status = 'rejected'
        print(f"Order {order.origin} -> {order.destination} timed out.")
        order_list.remove(order)  # Remove from the system

def process_orders(order_list, couriers):
    """
    Assigns orders to all available couriers.

    Parameters:
    - order_list (list): List of Order objects.
    - couriers (list): List of Courier objects.

    Returns:
    - None
    """
    for courier in couriers:
        assign_order_to_courier(order_list, courier)

def update_order_patience(order_list, m):
    """
    Updates the patience of each order and applies penalties for timed-out orders.

    Parameters:
    - order_list (list): List of Order objects.
    - m (float/int): Penalty value proportional to grid size.

    Returns:
    - timed_out_count (int): Number of orders that have timed out.
    """
    timed_out_orders = []
    timed_out_count = 0  # Initialize counter

    for order in order_list:
        if not order.assigned:
            order.patience -= 1
            if order.patience <= 0:
                timed_out_orders.append(order)
                timed_out_count += 1
                print(f"Order {order.origin} -> {order.destination} timed out.")

    # Remove timed-out orders from the order list
    for order in timed_out_orders:
        order.status = 'timed_out'
        order_list.remove(order)  # Remove from the system

    return timed_out_count

def generate_orders(num_orders, grid_length, patience=10):
    """
    Generates a specified number of orders with random origins and destinations.

    Parameters:
    - num_orders (int): Number of orders to generate.
    - grid_length (int): Length of the grid (assuming square grid).
    - patience (int): Patience duration for each order.

    Returns:
    - orders (list): List of generated Order objects.
    """
    orders = []
    for _ in range(num_orders):
        origin = (random.randint(0, grid_length - 1), random.randint(0, grid_length - 1))
        destination = (random.randint(0, grid_length - 1), random.randint(0, grid_length - 1))
        while destination == origin:
            destination = (random.randint(0, grid_length - 1), random.randint(0, grid_length - 1))
        orders.append(Order(origin=origin, destination=destination, patience=patience))
    return orders