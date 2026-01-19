"""
Script to split multi_agent_analysis.png into separate PNG files for each subplot
"""
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from pathlib import Path

def split_multi_agent_analysis():
    """
    Split the multi_agent_analysis.png file into separate PNG files
    """
    # Read the combined image
    img_path = Path('results/multi_agent_analysis.png')
    img = mpimg.imread(img_path)
    
    print(f"Image shape: {img.shape}")
    
    # The image typically has 2 rows and 3 columns of subplots
    # We'll split it into 6 separate images
    
    height, width = img.shape[:2]
    
    # Assuming 2 rows x 3 columns layout
    n_rows = 2
    n_cols = 3
    
    subplot_height = height // n_rows
    subplot_width = width // n_cols
    
    # Define subplot names based on typical multi-agent analysis
    subplot_names = [
        'productivity_trends',
        'sentiment_distribution', 
        'compliance_metrics',
        'interaction_patterns',
        'correlation_heatmap',
        'combined_insights'
    ]
    
    # Create output directory if it doesn't exist
    output_dir = Path('results/individual_plots')
    output_dir.mkdir(exist_ok=True)
    
    # Extract and save each subplot
    plot_idx = 0
    for row in range(n_rows):
        for col in range(n_cols):
            if plot_idx >= len(subplot_names):
                break
                
            # Calculate boundaries for this subplot
            y_start = row * subplot_height
            y_end = (row + 1) * subplot_height
            x_start = col * subplot_width
            x_end = (col + 1) * subplot_width
            
            # Extract subplot
            subplot_img = img[y_start:y_end, x_start:x_end]
            
            # Save subplot
            output_path = output_dir / f'{subplot_names[plot_idx]}.png'
            plt.figure(figsize=(10, 8))
            plt.imshow(subplot_img)
            plt.axis('off')
            plt.tight_layout(pad=0)
            plt.savefig(output_path, bbox_inches='tight', dpi=150)
            plt.close()
            
            print(f"Saved: {output_path}")
            plot_idx += 1
    
    print(f"\nSuccessfully split {plot_idx} subplots into {output_dir}")

if __name__ == '__main__':
    split_multi_agent_analysis()
