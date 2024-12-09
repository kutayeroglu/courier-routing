import random
import logging
import numpy as np

from core.order import Order
from utils.general_utils import manhattan_distance


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
            # Shuffle to randomize order among identical sorting keys
            random.shuffle(unassigned_orders)
            
            # Define a sort key that prioritizes:
            # 1. Distance from courier to order origin
            # 2. Distance from order origin to destination
            unassigned_orders.sort(
                key=lambda o: (
                    manhattan_distance(courier.location, o.origin),
                    manhattan_distance(o.origin, o.destination)
                )
            )

            # Select the nearest order based on the defined priority
            nearest_order = unassigned_orders[0]

            # Assign the order to the courier
            courier.current_order = nearest_order
            nearest_order.assigned = True
            courier.is_busy = True
            nearest_order.status = 'assigned'
            
            logging.debug(f"Courier at {courier.location} assigned to order {nearest_order.origin} -> {nearest_order.destination}")


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
        logging.debug(f"Order {order.origin} -> {order.destination} is back in the queue with patience {order.patience}.")
    else:
        order.status = 'rejected'
        logging.debug(f"Order {order.origin} -> {order.destination} timed out.")
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
                logging.debug(f"Order {order.origin} -> {order.destination} timed out.")

    # Remove timed-out orders from the order list
    for order in timed_out_orders:
        order.status = 'timed_out'
        order_list.remove(order)  # Remove from the system

    return timed_out_count

def generate_origin_destination_probs(grid_length):
    """
    Generates origin and destination probability maps based on grid size.
    Origins are center-weighted, destinations are edge-weighted.
    
    Parameters:
    - grid_length (int): Size of the grid (e.g., 3, 5, 8)
    
    Returns:
    - origin_prob (2D NumPy array): Probability map for origins
    - destination_prob (2D NumPy array): Probability map for destinations
    """
    # Create coordinate grids
    x = np.arange(grid_length)
    y = np.arange(grid_length)
    xv, yv = np.meshgrid(x, y, indexing='ij')
    
    # Calculate center coordinates
    center = ( (grid_length - 1) / 2, (grid_length - 1) / 2 )
    
    # Calculate Euclidean distance from center for each cell
    distances = np.abs(xv - center[0]) + np.abs(yv - center[1])
    
    # For origin_prob: Inverse distance with offset (closer to center -> higher probability)
    # Adding 1 to distance to avoid division by zero
    origin_weights = 1 / (distances + 1)
    origin_prob = origin_weights / origin_weights.sum()
    
    # For destination_prob: Direct distance (farther from center -> higher probability)
    destination_weights = distances
    # In case all distances are zero (grid_length=1), handle division by zero
    if destination_weights.sum() == 0:
        destination_prob = np.ones_like(destination_weights) / destination_weights.size
    else:
        destination_prob = destination_weights / destination_weights.sum()
    
    return origin_prob, destination_prob


def generate_orders(num_orders, grid_length, patience=10):
    """
    Generates a specified number of orders with random origins and destinations based on varying grid cell probabilities.
    
    Parameters:
    - num_orders (int): Number of orders to generate.
    - grid_length (int): Length of the grid (assuming square grid).
    - patience (int): Patience duration for each order.
    
    Returns:
    - orders (list): List of generated Order objects.
    """
    # Generate probability maps
    origin_prob, destination_prob = generate_origin_destination_probs(grid_length)
    
    # Flatten the grid cells and probability maps
    grid_cells = [(x, y) for x in range(grid_length) for y in range(grid_length)]
    origin_prob_flat = origin_prob.flatten()
    destination_prob_flat = destination_prob.flatten()
    
    # Generate orders
    orders = []
    for _ in range(num_orders):
        # Sample origin
        origin = random.choices(
            population=grid_cells,
            weights=origin_prob_flat,
            k=1
        )[0]
        
        # Sample destination
        destination = random.choices(
            population=grid_cells,
            weights=destination_prob_flat,
            k=1
        )[0]
        
        # Ensure destination is not the same as origin
        while destination == origin:
            destination = random.choices(
                population=grid_cells,
                weights=destination_prob_flat,
                k=1
            )[0]
        
        # Create and append the Order
        orders.append(Order(origin=origin, destination=destination, patience=patience))
    
    return orders