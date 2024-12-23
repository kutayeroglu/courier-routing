import random
import logging
from core.order import Order
from utils.order_utils import process_orders, update_order_patience
from utils.general_utils import plot_and_save_graphs
from learning.policy import epsilon_greedy
from core.action import take_action
from constants import patience_scale, max_num_orders


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


def simulate_couriers(couriers, order_list, q_table, m=5, max_steps=100):
    '''
    Simulates the actions of multiple couriers using the trained Q-table.

    Parameters:7z\
    - couriers: A list of Courier instances.
    - order_list: A list of Order objects.
    - q_table: The trained Q-table.
    - m (int/float): Parameter controlling reward magnitudes, proportional to grid size.
    - max_steps (int): Maximum number of steps in the simulation.

    Returns:
    - summary: Dictionary containing summary statistics.
    '''
    total_reward = 0
    # delivered_orders = 0
    # rejected_orders = 0
    # timed_out_orders = 0
    # initial_num_orders = len(order_list)
    episode_rewards = []
    episode_lengths = []
    courier = couriers

    for episode in range(1, 101):
        total_reward = 0

        # Reset courier's state
        courier.is_busy = False
        courier.current_order = None
        courier.location = (0, 0)

        # Reset orders
        order_list = generate_orders(max_num_orders, m, patience=patience_scale*m)

        # Assign orders at the start of the episode
        process_orders(order_list, [courier])

        for step in range(max_steps):
            # Check for terminal conditions (e.g., all orders delivered or timed out)
            if len(order_list) == 0:
                logging.debug(f"All orders have been processed.")
                # order_list = generate_orders(num_orders, m, patience=patience_scale*m)
                episode_rewards.append(total_reward)
                break

            # Get the current state
            state = (
                courier.location,
                courier.current_order.origin if courier.current_order else None,
                courier.current_order.destination if courier.current_order else None
            )

            # Choose an action using the epsilon-greedy policy with epsilon=0 (pure exploitation)
            action = epsilon_greedy(state, q_table, epsilon=0)

            # Execute the action and observe the next state and reward
            _, reward = take_action(courier, action, order_list, m)

            total_reward += reward

            # Show the courier's action, location, reward, and Q-value at each step
            # q_value = q_table.get((state, action), 0)
            # logging.debug(f"Courier {idx + 1}, Step {step + 1}: Action: {action}, Location: {courier.location}, Reward: {reward}, Q-value: {q_value}")

            # Update order patience and apply penalties for timed-out orders
            timed_out_count = update_order_patience(order_list)
            if timed_out_count > 0:
                penalty = timed_out_count * m
                total_reward -= penalty
        

        

    plot_and_save_graphs(episode_lengths, episode_rewards, str(m))


    summary = {
        'Total Reward': total_reward,
    }

    return summary