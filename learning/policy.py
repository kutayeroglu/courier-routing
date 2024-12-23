import random
from constants import actions
from core.action import get_illegal_actions

# Select an action based on epsilon-greedy policy
def epsilon_greedy(state, q_table, epsilon):
    """
    Selects an action based on the epsilon-greedy policy.

    With probability epsilon, selects a random action (exploration).
    With probability (1 - epsilon), selects the action(s) with the highest Q-value
    for the current state (exploitation). If multiple actions have the same maximum
    Q-value, one is selected at random.

    Parameters:
    - state: The current state of the agent.
    - q_table: A dictionary mapping (state, action) pairs to Q-values.
    - epsilon (float): The exploration rate (0 ≤ epsilon ≤ 1).

    Returns:
    - An action selected according to the epsilon-greedy policy.
    """
    assert 0 <= epsilon <= 1, "Epsilon must be between 0 and 1"
    assert len(actions) > 0, "The actions list must not be empty"

    # Find illegal actions and remove them from possible actions
    # illegal_actions = get_illegal_actions(state, grid_length)
    illegal_actions = []
    legal_actions = [action for action in actions if action not in illegal_actions]

    if random.uniform(0, 1) < epsilon: # Exploration
        return random.choice(legal_actions) 
    else: # Exploitation
        # Get Q-values for all actions in the current state
        q_values = [q_table.get((state, action), 0) for action in legal_actions]
        max_q_value = max(q_values)

        # Find all actions that have the max Q-value
        max_actions = [action for action, q in zip(legal_actions, q_values) if q == max_q_value]
        # Select randomly among them to break ties
        best_action = random.choice(max_actions)

        return best_action