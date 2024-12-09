
import numpy as np
from utils.order_utils import generate_orders, generate_origin_destination_probs

'''
In the paper it is stated that each grid's probability of becoming an order origin or order destination varies.
This script's purpose is to verify that the probability maps are valid.
'''

def verify_probabilities(origin_prob, destination_prob, tol=1e-6):
    """
    Verifies that the sum of probabilities in origin_prob and destination_prob equals 1.
    
    Parameters:
    - origin_prob (2D NumPy array): Probability map for origins.
    - destination_prob (2D NumPy array): Probability map for destinations.
    - tol (float): Tolerance for floating point comparison.
    
    Returns:
    - bool: True if both sums are approximately 1, False otherwise.
    """
    origin_sum = origin_prob.sum()
    destination_sum = destination_prob.sum()
    return np.isclose(origin_sum, 1.0, atol=tol) and np.isclose(destination_sum, 1.0, atol=tol)


for grid_length in [3, 5, 8]:
    num_orders = 10 * grid_length  # Example: number of orders scales with grid size
    orders = generate_orders(num_orders, grid_length, patience=10)
    
    # Verify probability maps
    origin_prob, destination_prob = generate_origin_destination_probs(grid_length)
    valid = verify_probabilities(origin_prob, destination_prob)
    print(f"Grid Size: {grid_length}x{grid_length}")
    print("Probability Maps Valid:", valid)
    
    # Analyze distribution
    analyze_order_distribution = lambda orders, grid_length: print(
        f"Origins: {np.unique([order.origin for order in orders], return_counts=True)}\n"
        f"Destinations: {np.unique([order.destination for order in orders], return_counts=True)}\n"
    )
    analyze_order_distribution(orders, grid_length)
    
    # Print first 5 orders for inspection
    print("First 5 Orders:")
    for idx, order in enumerate(orders[:5], 1):
        print(f"Order {idx}: Origin={order.origin}, Destination={order.destination}, Patience={order.patience}")
    print("-" * 50)
