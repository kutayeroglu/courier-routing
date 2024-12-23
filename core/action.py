import logging 
from constants import movement

# Take action and return the next state and reward
def take_action(courier, action, order_list, m=5):
    '''
    Description from paper:

    === Move ===
    * Each move action results in a reward of − 1 if an order is assigned to the courier
        * -0.1 otherwise.

    === Pick-up & Deliver ===
    * Couriers receive a positive reward for each successful pick-up and deliver
        actions. This reward is proportional to the grid size and adjusted to the
        total number of grids.

    * A penalty is incurred if the courier takes illegal pick-up and deliver actions.
        This penalty is also proportional to the grid size and adjusted to the total
        number of grids.
        * Note that illegal pick-up is defined as taking a pick-up action while there
        is no order in the courier location index. In addition, illegal deliver
        action may include the following situations:
            * taking a deliver action while there is no order with the courier
            * the courier location is not equal to destination.

    === Stay ===
    * If a courier takes a stay action, then no reward is received. However if
    a courier takes a stay action when an order is assigned to him, then a
    penalty is incurred, which is equal to the grid size.

    === Reject ===
    * Reject action also results in a negative reward. If the courier rejects an
    order while delivering it, a penalty is received, which is equal to the grid
    size.
        * On the other hand, if the courier rejects an order right after the order
        is assigned to it, then it receives a smaller penalty.

    === Timeout ===
    * It is also important to account for the timed-out orders in the environment,
    which might be byproduct of reject actions or having insufficient number of
    couriers.
        * In particular, if an order is not assigned to a courier within a predefined
        amount of time, then the order leaves the system and a penalty is incurred
        for each such order.
    '''
    reward = 0

    # Movement actions
    if action in ['up', 'down', 'left', 'right']:
        # Change order status if courier starts moving after assignment
        if courier.current_order and courier.current_order.status == 'assigned':
                courier.current_order.status = 'in_transit'

        dx, dy = movement[action]
        new_x = courier.location[0] + dx
        new_y = courier.location[1] + dy

        # Check grid boundaries
        if 0 <= new_x < m and 0 <= new_y < m:
            # Valid move; update location
            courier.location = (new_x, new_y)
            # Movement penalty: -1 if carrying an order, else -0.1
            reward = -1 if courier.current_order else -0.1
            logging.debug(f"Courier moved {action} to {courier.location}. Reward: {reward}")
        else:
            # Invalid move; do not move courier, assign a smaller penalty instead of -m
            reward = -(m**2)
            logging.debug(f"Courier attempted to move '{action}' out of bounds. Reward: {reward}")


    elif action == 'pick-up':
        if courier.current_order and courier.location == courier.current_order.origin:
            if not courier.current_order.status == 'assigned':
                # Successful pick-up
                reward = m ** 2  # Positive reward proportional to grid size
                courier.is_busy = True
                courier.current_order.status = 'in_transit'
            else:
                # Illegal pick-up (already assigned)
                reward = -(m ** 2)
                logging.debug("Illegal action: Attempted to pick up an already assigned order.")
        else:
            # Illegal pick-up (no order at location)
            reward = -(m**2)
            logging.debug("Illegal action: No order to pick up at current location.")


    elif action == 'deliver':
        if courier.current_order and courier.location == courier.current_order.destination:
            # Successful delivery
            reward = m ** 2  # Positive reward proportional to grid size
            courier.is_busy = False
            if courier.current_order in order_list:
                order_list.remove(courier.current_order)
            courier.current_order = None
        else:
            # Illegal delivery
            reward = -(m ** 2)
            logging.debug("Illegal action: No order to deliver at current location or wrong destination.")


    elif action == 'stay':
        if courier.current_order:
            # Penalty for staying while carrying an order
            reward = -(m ** 2)
            logging.debug("Penalty: Stayed while carrying an order.")
        else:
            # No reward or penalty for staying idle without an order
            reward = 0


    elif action == 'reject':
        if not courier.current_order:
            reward = -m / 3

        else: 
            # Reject in transit (order assigned, moved then rejected)
            if courier.current_order.status == 'in_transit':
                reward = -(m ** 2)
                logging.debug("Penalty: Rejected while delivering an order.")

            # Reject at beginning (order assigned, didn't move and rejected)
            if courier.current_order.status == 'assigned':
                reward = -m / 3
                logging.debug("Penalty: Rejected right after order assignment.")

            # Put order back in the waiting list
            courier.current_order.status = 'pending' 
            
            # Update courier status 
            courier.is_busy = False
            courier.current_order = None


    # Get next state
    next_state = (
        courier.location,
        courier.current_order.origin if courier.current_order else None,
        courier.current_order.destination if courier.current_order else None
    )

    return next_state, reward


def get_illegal_actions(state, grid_length):
    """
    Determine the set of legal actions based on the current state.

    Parameters:
    - state: Tuple containing (location, current_order_origin, current_order_destination)
    - actions: List of all possible actions

    Returns:
    - List of legal actions
    """
    courier_location, _, _ = state
    illegal_actions = []

    # Extract courier's current position
    x, y = courier_location

    # Define movement boundaries (assuming grid size m x m)
    m = grid_length

    # Movement actions
    if x == 0:
        illegal_actions.append('left')
    if x == m - 1:
        illegal_actions.append('right')
    if y == m-1:
        illegal_actions.append('up')
    if y == 0:
        illegal_actions.append('down')

    return illegal_actions
