import random
from order import Order
from order_utils import process_orders, update_order_patience
from policy import epsilon_greedy
from action import take_action


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


def simulate_couriers(couriers, order_list, q_table, grid_size=5, m=5, max_steps=100):
    '''
    Simulates the actions of multiple couriers using the trained Q-table.

    Parameters:
    - couriers: A list of Courier instances.
    - order_list: A list of Order objects.
    - q_table: The trained Q-table.
    - grid_size (int): Size of the grid (assuming square grid).
    - m (int/float): Parameter controlling reward magnitudes, proportional to grid size.
    - max_steps (int): Maximum number of steps in the simulation.

    Returns:
    - summary: Dictionary containing summary statistics.
    '''
    total_reward = 0
    delivered_orders = 0
    rejected_orders = 0
    timed_out_orders = 0
    initial_num_orders = len(order_list)

    for step in range(max_steps):
        # Assign orders to couriers if they are not busy
        process_orders(order_list, couriers)

        for idx, courier in enumerate(couriers):
            if not courier.is_busy and courier.current_order is None:
                # Get the current state
                state = (
                    courier.location,
                    courier.current_order.origin if courier.current_order else None,
                    courier.current_order.destination if courier.current_order else None
                )

                # Choose an action using the epsilon-greedy policy with epsilon=0 (pure exploitation)
                action = epsilon_greedy(state, q_table, epsilon=0)

                # Execute the action and observe the next state and reward
                next_state, reward = take_action(courier, action, order_list, m, grid_size)

                total_reward += reward

                # Show the courier's action, location, reward, and Q-value at each step
                q_value = q_table.get((state, action), 0)
                print(f"Courier {idx + 1}, Step {step + 1}: Action: {action}, Location: {courier.location}, Reward: {reward}, Q-value: {q_value}")

        # Update order patience and apply penalties for timed-out orders
        timed_out_count = update_order_patience(order_list, m)
        if timed_out_count > 0:
            penalty = timed_out_count * m
            total_reward -= penalty
            timed_out_orders += timed_out_count
            print(f"Applied penalty for {timed_out_count} timed-out order(s): -{penalty}")

        # Collect statistics
        delivered_orders = sum(1 for order in order_list if order.status == 'delivered')
        rejected_orders = sum(1 for order in order_list if order.status == 'rejected')

        # Check for terminal conditions (e.g., all orders delivered or timed out)
        if all(order.status in ['delivered', 'rejected', 'timed_out'] for order in order_list):
            print(f"All orders have been processed by step {step + 1}.")
            break

    summary = {
        'Total Reward': total_reward,
        'Delivered Orders': delivered_orders,
        'Rejected Orders': rejected_orders,
        'Timed-out Orders': timed_out_orders
    }

    print(f"\nSimulation Summary: {summary}")
    return summary