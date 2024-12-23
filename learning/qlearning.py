import logging

from core.action import take_action
from core.courier import Courier
from learning.policy import epsilon_greedy

from constants import actions, max_num_orders, patience_scale
from utils.general_utils import plot_and_save_graphs
from utils.order_utils import process_orders, update_order_patience, generate_orders


def q_learning(gamma=0.95,
               epsilon=0.5,
               max_episodes=2000,
               m=5,
               learning_rate=0.6,
               initial_num_orders=1,
               order_generation_interval=25):
    '''
    Trains a courier agent using the Q-learning algorithm.

    Parameters:
    - courier: An instance of the Courier class.
    - order_list: A list of Order objects.
    - q_table: A dictionary mapping (state, action) pairs to Q-values.
    - gamma (float): Discount factor for future rewards.
    - epsilon (float): Exploration rate for the epsilon-greedy policy.
    - max_episodes (int): Number of training episodes.
    - m (int/float): Parameter controlling reward magnitudes, proportional to grid size.

    Returns:
    - q_table: Updated Q-table after training.
    '''
    assert 0 <= gamma <= 1, "Discount factor (gamma) must be between 0 and 1"
    assert 0 <= epsilon <= 1, "Exploration rate (epsilon) must be between 0 and 1"

    q_table = {}
    episode_lengths = []
    episode_rewards = []
    min_lr = 0.01

    for episode in range(1, max_episodes + 1):
        decay_rate = (learning_rate - min_lr) / max_episodes
        current_lr = max(learning_rate - decay_rate * episode, min_lr)

        total_reward = 0
        episode_length = 0
        num_orders_created = 0

        # Initialize/reset courier
        courier = Courier((0, 0))

        # Reset orders
        order_list = generate_orders(initial_num_orders, m, patience=patience_scale*m)
        num_orders_created += initial_num_orders

        # Assign orders at the start of the episode
        process_orders(order_list, [courier])

        epsilon = max(epsilon - 0.002, 0.01)  # Decay epsilon

        max_step_size = (order_generation_interval * max_num_orders) + (patience_scale * m)
        # Loop over time steps in the episode
        for step in range(1, max_step_size):
            if step % order_generation_interval == 0:
                new_order = generate_orders(1, m, patience=patience_scale*m)
                num_orders_created += 1
                order_list.extend(new_order)

            # Check for terminal conditions (e.g., all orders delivered or timed out)
            if len(order_list) == 0 and num_orders_created == max_num_orders:
                logging.debug(f"All orders have been processed, generating new orders...")
                # order_list = generate_orders(num_orders, m, patience=patience_scale*m)
                break

            episode_length += 1

            # Get the current state
            state = (
                courier.location,
                courier.current_order.origin if courier.current_order else None,
                courier.current_order.destination if courier.current_order else None
            )

            # Choose an action using the epsilon-greedy policy
            action = epsilon_greedy(state, q_table, epsilon)

            # Execute the action and observe the next state and reward
            next_state, reward = take_action(courier, action, order_list)
            total_reward += reward

            # Update Q-value using Bellman equation with learning rate
            future_q_values = [q_table.get((next_state, a), 0) for a in actions]
            future_q_value = max(future_q_values) if future_q_values else 0
            current_q = q_table.get((state, action), 0)
            new_q_value = ((1 - current_lr) * current_q) + (learning_rate * (reward + gamma * future_q_value))
            # new_q_value = reward + gamma * future_q_value

            # Update the Q-table
            q_table[(state, action)] = new_q_value

            # Update order patience and apply penalties for timed-out orders
            timed_out_count = update_order_patience(order_list)
            if timed_out_count > 0:
                penalty = timed_out_count * (m**3)
                total_reward -= penalty
                logging.debug(f"Episode {episode + 1}, Step {step + 1}: Applied penalty for {timed_out_count} timed-out order(s): -{penalty}")

        # Save episode data for plotting
        episode_lengths.append(episode_length)
        episode_rewards.append(total_reward)

        logging.debug(f"Episode {episode + 1}: Total reward: {total_reward}\n")

    # Plot and save the graphs after training
    plot_and_save_graphs(episode_lengths, episode_rewards, str(m), simulation_run=False)
    
    return q_table
