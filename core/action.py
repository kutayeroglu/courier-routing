import logging 

from utils.order_utils import handle_rejected_order

# Take action and return the next state and reward
def take_action(courier, action, order_list, m, grid_size=5):
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


  # Action handling based on the defined reward structure
  if action == 'up':
      if courier.location[1] < grid_size - 1:
          courier.location = (courier.location[0], courier.location[1] + 1)
          reward = -1 if courier.current_order else -0.1
      else:
          reward = -m  # Penalty for illegal movement
          logging.debug("Illegal move: Cannot move up beyond grid boundaries.")

  elif action == 'down':
      if courier.location[1] > 0:
          courier.location = (courier.location[0], courier.location[1] - 1)
          reward = -1 if courier.current_order else -0.1
      else:
          reward = -m
          logging.debug("Illegal move: Cannot move down beyond grid boundaries.")

  elif action == 'left':
      if courier.location[0] > 0:
          courier.location = (courier.location[0] - 1, courier.location[1])
          reward = -1 if courier.current_order else -0.1
      else:
          reward = -m
          logging.debug("Illegal move: Cannot move left beyond grid boundaries.")

  elif action == 'right':
      if courier.location[0] < grid_size - 1:
          courier.location = (courier.location[0] + 1, courier.location[1])
          reward = -1 if courier.current_order else -0.1
      else:
          reward = -m
          logging.debug("Illegal move: Cannot move right beyond grid boundaries.")


  elif action == 'pick-up':
      if courier.current_order and courier.location == courier.current_order.origin:
          if not courier.current_order.assigned:
              # Successful pick-up
              reward = m ** 2  # Positive reward proportional to grid size
              courier.is_busy = True
              courier.current_order.assigned = True
              courier.current_order.status = 'in_transit'
          else:
              # Illegal pick-up (already assigned)
              reward = -m
              logging.debug("Illegal action: Attempted to pick up an already assigned order.")
      else:
          # Illegal pick-up (no order at location)
          reward = -m
          logging.debug("Illegal action: No order to pick up at current location.")

  elif action == 'deliver':
      if courier.current_order and courier.location == courier.current_order.destination:
          # Successful delivery
          reward = m ** 2  # Positive reward proportional to grid size
          courier.is_busy = False
          courier.current_order.status = 'delivered'
          if courier.current_order in order_list:
              order_list.remove(courier.current_order)
          courier.current_order = None
      else:
          # Illegal delivery
          reward = -m
          logging.debug("Illegal action: No order to deliver at current location or wrong destination.")

  elif action == 'stay':
      if courier.current_order:
          # Penalty for staying while carrying an order
          reward = -m
          logging.debug("Penalty: Stayed while carrying an order.")
      else:
          # No reward or penalty for staying idle without an order
          reward = 0

  elif action == 'reject':
      if courier.current_order:
          # Determine context for penalty differentiation
          if courier.is_busy:
              penalty = m  # Larger penalty for rejecting while delivering
              logging.debug("Penalty: Rejected while delivering an order.")
          else:
              penalty = m / 2  # Smaller penalty for rejecting right after assignment
              logging.debug("Penalty: Rejected right after order assignment.")
          handle_rejected_order(courier.current_order, order_list)
          reward = -penalty
          courier.is_busy = False
          courier.current_order = None
      else:
          # Penalty for rejecting without an assigned order
          reward = -m / 2  # Minimal penalty
          logging.debug("Penalty: Rejected when no order is assigned.")

  else:
      # Handle invalid actions
      reward = -m
      logging.debug(f"Invalid action '{action}' taken.")

  # Get next state
  next_state = (
      courier.location,
      courier.current_order.origin if courier.current_order else None,
      courier.current_order.destination if courier.current_order else None
  )

  return next_state, reward