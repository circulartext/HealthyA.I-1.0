import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import numpy as np

def visualize_combined(csv_file_intake, csv_file_adjustment):
    # Read the CSV files
    intake_data = pd.read_csv(csv_file_intake)
    adjustment_data = pd.read_csv(csv_file_adjustment)

    # Merge the datasets on the 'Nutrient' column using an outer join
    combined_data = pd.merge(intake_data, adjustment_data, on='Nutrient', how='outer')

    # Set the nutrient names as the index
    combined_data.set_index('Nutrient', inplace=True)

    # Define the number of charts per row
    charts_per_row = 5
    total_charts = len(combined_data)
    rows = (total_charts + charts_per_row - 1) // charts_per_row

    # Create a figure with a grid layout
    fig, axes = plt.subplots(rows, charts_per_row, figsize=(15, rows * 3), gridspec_kw={'hspace': 0.6, 'wspace': 0.5})

    # Flatten axes for easier iteration
    axes = axes.flatten()

    # Iterate over each nutrient and its data
    for i, (nutrient, row) in enumerate(combined_data.iterrows()):
        ax = axes[i]

        # Plot the intake bars
        bar_colors = ['blue', 'lightgray', 'gray']
        bar_labels = ['Intake', 'Min RDI', 'Max RDI']
        bar_values = [
            row.get('Intake', 0),
            row.get('Min RDI', 0),
            row.get('Max RDI', 0)
        ]
        ax.bar(bar_labels, bar_values, color=bar_colors, width=0.5)

        # Extract and plot the adjustment value as a line if it exists
        adjustment_position = None
        if pd.notna(row.get('Adjustment')):
            adjustment_value = float(row['Adjustment'].split(' ')[2])
            action = 'Increase' if 'Increase' in row['Adjustment'] else 'Decrease'
            adjustment_color = 'orange' if action == 'Increase' else 'red'

            # Calculate line position and ensure it aligns with the adjustment type
            adjustment_position = bar_values[0] + adjustment_value if action == 'Increase' else bar_values[0] - adjustment_value
            ax.axhline(adjustment_position, color=adjustment_color, linestyle='--', linewidth=2)

            # Add adjustment annotation
            ax.text(1.5, adjustment_position + (max(bar_values) * 0.05 if action == 'Increase' else -max(bar_values) * 0.05), 
                    f'{adjustment_value:.1f}', ha='center', fontsize=8, color=adjustment_color)

        # Set the y-axis limits
        max_value = max(bar_values + [adjustment_position if adjustment_position is not None else 0])
        if not np.isnan(max_value) and not np.isinf(max_value):
            ax.set_ylim(0, max_value * 1.2)

        # Add titles and labels
        ax.set_title(f'{nutrient}', fontsize=10)
        ax.set_ylabel('Amount', fontsize=8)
        ax.tick_params(axis='both', labelsize=8)
        ax.yaxis.set_major_locator(MaxNLocator(5))

        # Add value annotations on bars
        for idx, value in enumerate(bar_values):
            ax.text(idx, value + (max_value * 0.05), f'{value:.1f}', ha='center', fontsize=8)

    # Turn off any unused subplots
    for j in range(total_charts, len(axes)):
        axes[j].axis('off')

    # Add a shared x-axis label at the bottom
    fig.text(0.5, 0.02, 'Nutrient Categories', ha='center', fontsize=12)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Example usage: visualize combined CSV files
    visualize_combined('nutrient_intake_results.csv', 'ideal_adjustments.csv')
