import numpy as np
import random

from .constants import simulation_parameters, num_orders
from .courier import Courier
from .order_utils import generate_orders
from .qlearning import q_learning
from .simulation_utils import simulate_couriers

# Set random seed for reproducibility
random.seed(42)


def main_simulation():
    '''
        As the state space becomes larger, visiting each system state and generating
        optimal actions for those tend to become challenging. That is, as our model
        involves multiple couriers and their concurrent locations in the grid, the state
        space becomes intractable for increasing the number of couriers and grid sizes.
        As a result, Q-learning algorithm might fail to learn optimal policy for large
        problem instances. In order to overcome this issue, we devise a solution mechanism
        that simplifies the overall problem. Specifically, we use Q-learning algorithm
        to train just one courier for various grid sizes. The resulting policy is then
        used for each courier in the system.
    '''

    for grid_size_total, num_couriers in simulation_parameters:
        grid_length = int(np.sqrt(grid_size_total))
        
        if grid_length ** 2 != grid_size_total:
            print(f"Warning: Grid size {grid_size_total} is not a perfect square. Interpreting grid_length as {grid_length}.")

        m = grid_length

        print(f"\n=== Simulation for Grid Size: {grid_size_total} (Grid Length: {grid_length}x{grid_length}), Number of Couriers: {num_couriers} ===")

        # Initialize Q-table
        q_table = {}

        # Initialize one courier for training
        training_courier = Courier((0, 0))  # Starting at (0,0)

        # Generate orders for training
        training_order_list = generate_orders(num_orders, grid_length, patience=10)

        # Train Q-learning for the current grid size
        print(f"Training Q-learning for grid size {grid_size_total} with 1 courier...")
        trained_q_table = q_learning(
            training_courier,
            training_order_list,
            q_table,
            gamma=0.9,
            epsilon=0.1,
            max_episodes=1000,
            grid_size=grid_length,
            m=m
        )

        # Now, run simulations with the trained Q-table
        for simulation_run in range(1, 3):  # Run two simulations: one for 1 courier, one for 2 couriers
            # Initialize couriers
            couriers = [Courier((0, 0)) for _ in range(num_couriers)]  # All start at (0,0)

            # Generate a fresh set of orders for the simulation
            simulation_order_list = generate_orders(num_orders, grid_length, patience=10)

            print(f"\nRunning simulation {simulation_run} with {num_couriers} courier(s) on grid size {grid_size_total}...")
            summary = simulate_couriers(
                couriers,
                simulation_order_list,
                trained_q_table,
                grid_size=grid_length,
                m=m,
                max_steps=100
            )

            print(f"Simulation {simulation_run} Result: {summary}")

if __name__ == "__main__":
    main_simulation()