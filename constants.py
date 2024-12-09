'''
- First four actions define the movement direction in the grid.

- Deliver & Pick-up:
  A courier is expected to:
    a. pick up an order when its location coincides with the origin of an order.
    b. take deliver action when a courier location is equal to an order destination
    and the courier picked up this order from its origin before.

- Stay:
  A courier may stay on its current location when there is no order assigned to it.
  
- Reject:
  Reject action can be taken if an order is just assigned to a courier and courier
  does not start his movement.
    a. If a courier takes reject action, then that order is returned to the order
    list and it can be assigned to another courier.
'''
actions = ['up', 'down', 'left', 'right', 'pick-up', 'deliver', 'stay', 'reject']


# Define simulation parameters: (grid_size_total, number_of_couriers, episode_number)
simulation_parameters = [
    # (9, 1, 1000),
    # (9, 2, 1000),
    (25, 1, 2000),
    # (25, 2, 2000),
    # (64, 1, 4000),
    # (64, 2, 4000)
]


# Number of orders per simulation
num_orders = 10


# dx, dy for directions
movement = {
    'up': (0, 1),
    'down': (0, -1),
    'left': (-1, 0),
    'right': (1, 0)
}