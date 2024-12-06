from order_utils import process_orders
from policy import epsilon_greedy
from action import take_action
from constants import actions
from order_utils import update_order_patience

def q_learning(courier, order_list, q_table, gamma=0.9, epsilon=0.1, max_episodes=1000, grid_size=5, m=5):
    '''
    Trains a courier agent using the Q-learning algorithm.

    Parameters:
    - courier: An instance of the Courier class.
    - order_list: A list of Order objects.
    - q_table: A dictionary mapping (state, action) pairs to Q-values.
    - gamma (float): Discount factor for future rewards.
    - epsilon (float): Exploration rate for the epsilon-greedy policy.
    - max_episodes (int): Number of training episodes.
    - grid_size (int): Size of the grid (assuming square grid).
    - m (int/float): Parameter controlling reward magnitudes, proportional to grid size.

    Returns:
    - q_table: Updated Q-table after training.
    '''
    assert 0 <= gamma <= 1, "Discount factor (gamma) must be between 0 and 1"
    assert 0 <= epsilon <= 1, "Exploration rate (epsilon) must be between 0 and 1"

    for episode in range(max_episodes):
        total_reward = 0

        # Reset courier's state
        courier.is_busy = False
        courier.current_order = None
        courier.location = (0, 0)  # Reset to starting location

        # Reset orders
        for order in order_list:
            order.assigned = False
            order.status = 'pending'

        # Assign orders at the start of the episode
        process_orders(order_list, [courier])

        # Loop over time steps in the episode
        for step in range(100):  # max steps per episode
            # Get the current state
            state = (
                courier.location,
                courier.current_order.origin if courier.current_order else None,
                courier.current_order.destination if courier.current_order else None
            )

            # Choose an action using the epsilon-greedy policy
            action = epsilon_greedy(state, q_table, epsilon)

            # Execute the action and observe the next state and reward
            next_state, reward = take_action(courier, action, order_list, m, grid_size)

            # Update Q-value using Bellman equation
            future_q_values = [q_table.get((next_state, a), 0) for a in actions]
            future_q_value = max(future_q_values) if future_q_values else 0
            new_q_value = reward + gamma * future_q_value

            # Update the Q-table
            q_table[(state, action)] = round(new_q_value, 2)

            total_reward += reward

            # Update order patience and apply penalties for timed-out orders
            timed_out_count = update_order_patience(order_list, m)
            if timed_out_count > 0:
                penalty = timed_out_count * m
                total_reward -= penalty
                print(f"Episode {episode + 1}, Step {step + 1}: Applied penalty for {timed_out_count} timed-out order(s): -{penalty}")

            # Show the courier's action, location, reward, and Q-value at each step
            q_value = q_table.get((state, action), 0)
            print(f"Episode {episode + 1}, Step {step + 1}: Action: {action}, Location: {courier.location}, Reward: {reward}, Q-value: {q_value}")

            # Check for terminal conditions (e.g., all orders delivered or timed out)
            if all(order.status in ['delivered', 'rejected', 'timed_out'] for order in order_list):
                print(f"Episode {episode + 1}: All orders have been processed by step {step + 1}.")
                break

        print(f"Episode {episode + 1}: Total reward: {total_reward}\n")

    return q_table
