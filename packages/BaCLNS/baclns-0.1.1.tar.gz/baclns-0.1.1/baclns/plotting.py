import matplotlib.pyplot as plt
import os

def plot_responses(time, state_values, control_inputs, errors, save_folder=None):
    # Plot state variables
    plt.figure(figsize=(8, 6))
    
    for i, state in enumerate(state_values):
        plt.plot(time, state, label=f'State x{i+1}')
    
    plt.xlabel('Time (s)')
    plt.ylabel('States')
    plt.title('System Response')
    plt.grid(True)
    plt.legend()
    
    # Save the plot if save_folder is specified
    if save_folder:
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)
        plt.savefig(os.path.join(save_folder, 'system_response.png'))

    plt.figure(figsize=(8, 6))
    
    # Plot control inputs
    plt.plot(time[:-1], control_inputs, label='Control Input u')
    
    plt.xlabel('Time (s)')
    plt.ylabel('Control Input')
    plt.title('System Control Input')
    plt.grid(True)
    plt.legend()
    
    # Save the plot if save_folder is specified
    if save_folder:
        plt.savefig(os.path.join(save_folder, 'control_input.png'))
    
    plt.figure(figsize=(8, 6))
    
    # Plot errors
    for i, error_list in enumerate(zip(*errors)):
        plt.plot(time[:-1], error_list, label=f'Error in State x{i+1}')
    
    plt.xlabel('Time (s)')
    plt.ylabel('Error')
    plt.title('State Errors Over Time')
    plt.grid(True)
    plt.legend()
    
    # Save the plot if save_folder is specified
    if save_folder:
        plt.savefig(os.path.join(save_folder, 'state_errors.png'))
    
    # Show all plots
    plt.show()
