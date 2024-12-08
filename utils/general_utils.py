import os
import logging 

import matplotlib.pyplot as plt


# Helper function to calculate Manhattan distance
def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def plot_and_save_graphs(episode_lengths, episode_rewards, grid_name, number_of_couriers):
    '''
    Plots and saves two graphs:
    - Episode number vs Episode length
    - Episode number vs Collected reward

    Parameters:
    - episode_lengths (list): List of episode lengths.
    - episode_rewards (list): List of total rewards per episode.
    - grid_name (str): Name of the grid (for filename purposes).
    - number_of_couriers (str): Number of couriers the simulation is run with.

    Returns:
    - None
    '''
    # Create a directory to save plots if it doesn't exist
    plots_dir = 'plots'
    os.makedirs(plots_dir, exist_ok=True)

    # Define filenames with grid and courier names
    episode_length_filename = f"episode_length_{grid_name}_{number_of_couriers}.png"
    episode_reward_filename = f"episode_reward_{grid_name}_{number_of_couriers}.png"

    # Plot Episode Length vs Episode Number
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, len(episode_lengths) + 1), episode_lengths, label='Episode Length')
    plt.xlabel('Episode Number')
    plt.ylabel('Episode Length (Steps)')
    plt.title(f'Episode Length vs Episode Number\nGrid: {grid_name}, Courier: {number_of_couriers}')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, episode_length_filename))
    plt.close()

    # Plot Episode Reward vs Episode Number
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, len(episode_rewards) + 1), episode_rewards, label='Total Reward', color='orange')
    plt.xlabel('Episode Number')
    plt.ylabel('Total Reward')
    plt.title(f'Total Reward vs Episode Number\nGrid: {grid_name}, Courier: {number_of_couriers}')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, episode_reward_filename))
    plt.close()

    logging.getLogger('plot_and_save_graphs').info(f"Saved plots: {episode_length_filename}, {episode_reward_filename}")