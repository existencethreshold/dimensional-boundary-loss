"""
PUBLICATION FIGURES GENERATOR - MULTI-SIZE VERSION (FIXED LAYOUTS)
Complete figure generation for dimensional cascade validation across multiple grid sizes

Generates 7 publication-quality figures from multi-size validation data

Author: Nathan M. Thornhill
Date: January 2026
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Polygon
import seaborn as sns
import json
from pathlib import Path

# Set publication-quality style
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.size'] = 11
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.labelsize'] = 13
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.titlepad'] = 15
plt.rcParams['xtick.labelsize'] = 11
plt.rcParams['ytick.labelsize'] = 11
plt.rcParams['legend.fontsize'] = 10
plt.rcParams['figure.titlesize'] = 16

COLORS = {
    'primary': '#0173B2',
    'secondary': '#DE8F05',
    'success': '#029E73',
    'danger': '#CC78BC',
    'gray': '#949494',
    '1d2d': '#0173B2',
    '2d3d': '#DE8F05',
    '3d4d': '#029E73'
}


def load_multisize_data():
    """Load multi-size validation data"""
    data_dir = Path(__file__).parent / "validation_results_multisize"
    
    try:
        # Load summary file
        summary_files = list(data_dir.glob("multisize_summary_*.json"))
        if not summary_files:
            print("\n" + "="*70)
            print("❌ MISSING FILE: multisize_summary_*.json")
            print("="*70)
            print("\nPlease run the multi-size validation first:")
            print("  python validate_dimensional_cascade_multisize.py")
            print("="*70)
            return None
        
        summary_file = summary_files[0]
        with open(summary_file, 'r') as f:
            summary_data = json.load(f)
        
        # Load individual grid files for detailed pattern data
        grid_data = {}
        for grid_size in [15, 17, 20, 23, 25]:
            grid_files = list(data_dir.glob(f"dimensional_cascade_N100_grid{grid_size}_*.json"))
            if grid_files:
                with open(grid_files[0], 'r') as f:
                    grid_data[grid_size] = json.load(f)
        
        print("\n" + "="*70)
        print("DATA LOADED SUCCESSFULLY")
        print("="*70)
        print(f"Summary file: {summary_file.name}")
        print(f"Grid data loaded: {list(grid_data.keys())}")
        print(f"Total patterns: {summary_data['metadata']['total_patterns']}")
        print("="*70 + "\n")
        
        return summary_data, grid_data
        
    except Exception as e:
        print(f"\n❌ ERROR loading data: {e}")
        return None


def generate_figure_1_conceptual():
    """Figure 1: Conceptual overview - FIXED with proper spacing"""
    
    fig = plt.figure(figsize=(18, 6))
    
    # Create 3 subplots with more space
    ax1 = plt.subplot(1, 3, 1)
    ax2 = plt.subplot(1, 3, 2)
    ax3 = plt.subplot(1, 3, 3)
    
    axes = [ax1, ax2, ax3]
    
    transitions = [
        ('1D→2D', '85.8%', COLORS['1d2d']),
        ('2D→3D', '86.1%', COLORS['2d3d']),
        ('3D→4D', '86.1%', COLORS['3d4d'])
    ]
    
    for idx, (ax, (title, loss, color)) in enumerate(zip(axes, transitions)):
        ax.clear()
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        
        # Add colored box
        box = FancyBboxPatch((0.15, 0.35), 0.7, 0.3, 
                             boxstyle="round,pad=0.02", 
                             edgecolor=color, facecolor=color, 
                             alpha=0.2, linewidth=3)
        ax.add_patch(box)
        
        # Title (well above box)
        ax.text(0.5, 0.8, title, 
               ha='center', va='center', 
               fontsize=28, fontweight='bold', color=color)
        
        # Loss text (in box)
        ax.text(0.5, 0.5, f'{loss} Loss', 
               ha='center', va='center', 
               fontsize=18, fontweight='bold', color=color)
    
    plt.suptitle('Dimensional Cascade: Information Loss at Boundaries', 
                fontsize=20, fontweight='bold', y=0.98)
    
    plt.tight_layout(rect=[0, 0.02, 1, 0.94])
    return fig


def generate_figure_2_distribution(grid_data):
    """Figure 2: Loss distribution across all patterns"""
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Collect all losses from all grid sizes
    all_losses = []
    
    for grid_size, data in grid_data.items():
        all_losses.extend([r['loss_pct'] for r in data['test_1d_2d']])
        all_losses.extend([r['loss_pct'] for r in data['test_2d_3d']])
        all_losses.extend([r['loss_pct'] for r in data['test_3d_4d']])
    
    # Create histogram
    ax.hist(all_losses, bins=30, alpha=0.7, color=COLORS['primary'], edgecolor='black')
    
    # Add mean line
    mean_loss = np.mean(all_losses)
    ax.axvline(mean_loss, color='red', linestyle='--', linewidth=2, label=f'Mean: {mean_loss:.1f}%')
    
    # Add 86% reference line
    ax.axvline(86, color='green', linestyle=':', linewidth=2, label='Expected: 86%')
    
    ax.set_xlabel('Information Loss (%)', fontsize=13)
    ax.set_ylabel('Frequency', fontsize=13)
    ax.set_title('Distribution of Information Loss Across All Transitions and Grid Sizes\n(N=1,500 patterns)', 
                 fontsize=14, fontweight='bold')
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig


def generate_figure_3_rule_independence(summary_data):
    """Figure 3: Rule independence - Conway vs HighLife with actual data"""
    
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Load actual validation data
    # Conway data: Use grid_20, 2D→3D transition from multisize validation
    conway_loss = summary_data['results_by_size']['grid_20']['test_2d_3d']['mean_loss_pct']
    
    # HighLife data: Load from validation file
    try:
        highlife_file = Path(__file__).parent / "tests" / "validation_data" / "highlife_validation_20260113_035936.json"
        with open(highlife_file, 'r') as f:
            highlife_data = json.load(f)
        highlife_loss = highlife_data['statistics']['mean_loss']
    except FileNotFoundError:
        # Fallback to documented value if file not found
        print("⚠️  Warning: HighLife validation file not found, using documented value 87.11%")
        highlife_loss = 87.11
    
    rules = ['Conway\n(B3/S23)', 'HighLife\n(B36/S23)']
    losses = [conway_loss, highlife_loss]
    colors = [COLORS['primary'], COLORS['secondary']]
    
    bars = ax.bar(rules, losses, color=colors, alpha=0.7, edgecolor='black', linewidth=2)
    
    # Add value labels
    for bar, loss in zip(bars, losses):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{loss:.1f}%', ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    ax.set_ylabel('Mean Information Loss (%)', fontsize=13)
    ax.set_title('Rule Independence: Conway vs HighLife\n(Geometric effect independent of dynamics)', 
                 fontsize=14, fontweight='bold')
    ax.set_ylim(0, 100)
    ax.axhline(86, color='gray', linestyle='--', linewidth=1, alpha=0.5, label='Expected: 86%')
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    return fig


def generate_figure_4_grid_robustness(summary_data):
    """Figure 4: Grid size robustness analysis"""
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    grid_sizes = [15, 17, 20, 23, 25]
    
    # Extract mean loss for each grid size
    losses_1d2d = []
    losses_2d3d = []
    losses_3d4d = []
    
    for grid_size in grid_sizes:
        grid_key = f'grid_{grid_size}'
        losses_1d2d.append(summary_data['results_by_size'][grid_key]['test_1d_2d']['mean_loss_pct'])
        losses_2d3d.append(summary_data['results_by_size'][grid_key]['test_2d_3d']['mean_loss_pct'])
        losses_3d4d.append(summary_data['results_by_size'][grid_key]['test_3d_4d']['mean_loss_pct'])
    
    # Plot lines with markers
    ax.plot(grid_sizes, losses_1d2d, 'o-', color=COLORS['1d2d'], linewidth=2, markersize=8, label='1D→2D')
    ax.plot(grid_sizes, losses_2d3d, 's-', color=COLORS['2d3d'], linewidth=2, markersize=8, label='2D→3D')
    ax.plot(grid_sizes, losses_3d4d, '^-', color=COLORS['3d4d'], linewidth=2, markersize=8, label='3D→4D')
    
    # Add 86% reference line
    ax.axhline(86, color='gray', linestyle='--', linewidth=2, alpha=0.7, label='Expected: 86%')
    
    # Add shaded region
    ax.axhspan(82, 90, alpha=0.1, color='green', label='Acceptable Range')
    
    ax.set_xlabel('Grid Size (N)', fontsize=13)
    ax.set_ylabel('Mean Information Loss (%)', fontsize=13)
    ax.set_title('Grid Size Robustness: Scale-Independent ~86% Loss\n(100 patterns per grid size per transition)', 
                 fontsize=14, fontweight='bold')
    ax.set_xticks(grid_sizes)
    ax.set_ylim(80, 92)
    ax.legend(fontsize=11, loc='best')
    ax.grid(True, alpha=0.3)
    
    # Add stats annotation
    overall_mean = summary_data['consistency_analysis']['test_1d_2d']['mean_across_sizes']
    cv = summary_data['consistency_analysis']['test_1d_2d']['coefficient_of_variation']
    ax.text(0.98, 0.02, f'Overall Mean: {overall_mean:.1f}%\nCV: {cv:.2f}%', 
            transform=ax.transAxes, ha='right', va='bottom',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5), fontsize=10)
    
    plt.tight_layout()
    return fig


def generate_figure_5_phi_components(grid_data):
    """Figure 5: Φ metric components - FIXED with better spacing"""
    
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    
    # Use N=20 data
    data_20 = grid_data[20]
    
    transitions = [
        ('1D→2D', data_20['test_1d_2d']),
        ('2D→3D', data_20['test_2d_3d']),
        ('3D→4D', data_20['test_3d_4d'])
    ]
    
    for col, (trans_name, trans_data) in enumerate(transitions):
        # R component (top row)
        ax_r = axes[0, col]
        r_lower = [r['R_lower'] for r in trans_data]
        r_higher = [r['R_higher'] for r in trans_data]
        
        ax_r.hist([r_lower, r_higher], bins=20, 
                 label=['Native', 'Embedded'], 
                 alpha=0.7, color=['#0173B2', '#DE8F05'],
                 edgecolor='black', linewidth=0.5)
        ax_r.set_title(f'{trans_name}: R (Processing)', 
                      fontsize=14, fontweight='bold', pad=15)
        ax_r.set_xlabel('R Value', fontsize=12)
        ax_r.set_ylabel('Frequency', fontsize=12)
        ax_r.legend(fontsize=10, loc='upper right', framealpha=0.9)
        ax_r.grid(True, alpha=0.3, linewidth=0.5)
        
        # S component (bottom row)
        ax_s = axes[1, col]
        s_lower = [r['S_lower'] for r in trans_data]
        s_higher = [r['S_higher'] for r in trans_data]
        
        ax_s.hist([s_lower, s_higher], bins=20, 
                 label=['Native', 'Embedded'], 
                 alpha=0.7, color=['#029E73', '#CC78BC'],
                 edgecolor='black', linewidth=0.5)
        ax_s.set_title(f'{trans_name}: S (Integration)', 
                      fontsize=14, fontweight='bold', pad=15)
        ax_s.set_xlabel('S Value', fontsize=12)
        ax_s.set_ylabel('Frequency', fontsize=12)
        ax_s.legend(fontsize=10, loc='upper right', framealpha=0.9)
        ax_s.grid(True, alpha=0.3, linewidth=0.5)
    
    fig.suptitle('Φ Metric Components: R and S Across Dimensional Transitions\n(Grid Size N=20, 100 patterns per transition)', 
                fontsize=18, fontweight='bold', y=0.98)
    
    plt.tight_layout(rect=[0, 0.02, 1, 0.96])
    return fig


def generate_figure_6_visual_example(grid_data):
    """Figure 6: Visual example - FIXED with proper spacing"""
    
    fig = plt.figure(figsize=(18, 7))
    
    # Create grid with extra space for labels
    gs = fig.add_gridspec(1, 3, wspace=0.4, hspace=0.4,
                          left=0.05, right=0.95, top=0.85, bottom=0.15)
    
    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[0, 1])
    ax3 = fig.add_subplot(gs[0, 2])
    
    # Get first pattern from N=20 data
    data_20 = grid_data[20]
    pattern_0 = data_20['test_1d_2d'][0]
    
    # Recreate pattern
    np.random.seed(100)
    pattern_1d = np.random.randint(0, 2, size=20)
    pattern_2d = np.zeros((20, 20), dtype=int)
    pattern_2d[10, :] = pattern_1d
    
    # Plot 1: 1D pattern
    ax1.imshow(pattern_1d.reshape(1, -1), cmap='binary', aspect='auto', interpolation='nearest')
    ax1.set_title('1D Pattern (Native)', fontsize=14, fontweight='bold', pad=10)
    ax1.set_xlabel('Cell Position', fontsize=12)
    ax1.set_yticks([])
    
    # Plot 2: 2D embedding
    ax2.imshow(pattern_2d, cmap='binary', interpolation='nearest')
    ax2.set_title('2D Embedding (Middle Row)', fontsize=14, fontweight='bold', pad=10)
    ax2.set_xlabel('X Position', fontsize=12)
    ax2.set_ylabel('Y Position', fontsize=12)
    ax2.axhline(10, color='red', linestyle='--', linewidth=2, alpha=0.5)
    
    # Plot 3: Information budget
    categories = ['Retained', 'Lost']
    values = [100 - pattern_0['loss_pct'], pattern_0['loss_pct']]
    colors = ['#029E73', '#CC78BC']
    
    bars = ax3.barh(categories, values, color=colors, alpha=0.8, edgecolor='black', linewidth=2)
    ax3.set_title('Information Budget', fontsize=14, fontweight='bold', pad=10)
    ax3.set_xlabel('Percentage (%)', fontsize=12)
    ax3.set_xlim(0, 100)
    ax3.grid(True, alpha=0.3, axis='x')
    
    # Add value labels
    for bar, val in zip(bars, values):
        width = bar.get_width()
        ax3.text(width/2, bar.get_y() + bar.get_height()/2, 
                f'{val:.1f}%', 
                ha='center', va='center', 
                fontsize=14, fontweight='bold',
                color='white' if val > 50 else 'black')
    
    # Title at top
    fig.suptitle('Visual Example: 1D→2D Dimensional Embedding (Pattern ID 0, Grid Size 20)', 
                fontsize=18, fontweight='bold', y=0.95)
    
    # Stats at bottom (well below plots)
    stats_text = f"Φ(1D) = {pattern_0['phi_lower']:.3f}  →  Φ(2D) = {pattern_0['phi_higher']:.3f}  |  Loss = {pattern_0['loss_pct']:.1f}%"
    fig.text(0.5, 0.05, stats_text, ha='center', fontsize=13, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.7, pad=0.7))
    
    return fig


def generate_figure_7_reverse_prism():
    """Figure 7: Reverse Prism with actual diagrams - FIXED"""
    
    fig = plt.figure(figsize=(18, 10))
    
    # Create two side-by-side panels
    ax_left = plt.subplot(1, 2, 1)
    ax_right = plt.subplot(1, 2, 2)
    
    # LEFT PANEL: Traditional Prism
    ax_left.set_xlim(0, 10)
    ax_left.set_ylim(0, 10)
    ax_left.axis('off')
    
    # Draw prism (triangle)
    prism = Polygon([(2, 3), (2, 7), (4, 5)], 
                    closed=True, fill=True, 
                    facecolor='lightblue', edgecolor='black', linewidth=2)
    ax_left.add_patch(prism)
    
    # Input beam (white light)
    ax_left.arrow(0.5, 5, 1.3, 0, head_width=0.3, head_length=0.2, 
                 fc='white', ec='black', linewidth=2)
    ax_left.text(1, 6, 'White Light\n(1 Beam)', ha='center', fontsize=12, fontweight='bold')
    
    # Output spectrum (rainbow)
    spectrum_colors = ['#FF0000', '#FF7F00', '#FFFF00', '#00FF00', '#0000FF', '#4B0082', '#9400D3']
    for i, color in enumerate(spectrum_colors):
        y_offset = (i - 3) * 0.5
        ax_left.arrow(4, 5, 2.5, y_offset, head_width=0.2, head_length=0.2,
                     fc=color, ec='black', linewidth=1.5, alpha=0.8)
    
    ax_left.text(7.5, 5, 'Spectrum\n(7 Colors)', ha='center', fontsize=12, fontweight='bold')
    
    # Label
    ax_left.text(5, 9, 'Traditional Prism', 
                ha='center', fontsize=16, fontweight='bold',
                bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8, pad=0.5))
    ax_left.text(5, 8, 'Dimension Increase: 1D → Multi-D', 
                ha='center', fontsize=13, style='italic')
    
    # RIGHT PANEL: Reverse Prism
    ax_right.set_xlim(0, 10)
    ax_right.set_ylim(0, 10)
    ax_right.axis('off')
    
    # Draw inverted prism
    prism_inv = Polygon([(6, 5), (8, 3), (8, 7)], 
                        closed=True, fill=True,
                        facecolor='lightcoral', edgecolor='black', linewidth=2)
    ax_right.add_patch(prism_inv)
    
    # Input: high-dimensional (multiple beams)
    input_colors = ['purple', 'purple', 'purple', 'purple', 'purple', 'purple', 'purple']
    for i, color in enumerate(input_colors):
        y_offset = (i - 3) * 0.5
        ax_right.arrow(2, 5 + y_offset, 3.8, -y_offset, head_width=0.2, head_length=0.2,
                      fc=color, ec='black', linewidth=1.5, alpha=0.6)
    
    ax_right.text(2, 2, 'Neural Activity\n(High-D)', 
                 ha='center', fontsize=12, fontweight='bold')
    
    # Output: 3D conscious experience (single beam)
    ax_right.arrow(8, 5, 1.3, 0, head_width=0.3, head_length=0.2,
                  fc='gold', ec='black', linewidth=2)
    ax_right.text(9, 6, '3D Experience\n(Awareness)', 
                 ha='center', fontsize=12, fontweight='bold')
    
    # Label
    ax_right.text(5, 9, 'Reverse Prism Hypothesis', 
                 ha='center', fontsize=16, fontweight='bold',
                 bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.8, pad=0.5))
    ax_right.text(5, 8, 'Dimension Reduction: High-D → 3D', 
                 ha='center', fontsize=13, style='italic')
    
    # Central annotation (86% loss)
    fig.text(0.5, 0.5, '⬇ 86% INFORMATION LOSS AT EACH BOUNDARY ⬇', 
            ha='center', va='center', fontsize=18, fontweight='bold', color='red',
            bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.9, pad=1.0))
    
    # Bottom implications (well below)
    implications = """Implications for Consciousness:
• High-dimensional neural substrate → Low-dimensional phenomenal experience
• 86% of substrate information never reaches conscious awareness  
• Dimensional dispersion as fundamental filter of consciousness
• Explains the "hard problem": Most information is geometrically lost"""
    
    fig.text(0.5, 0.08, implications, ha='center', fontsize=12,
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.7, pad=0.8))
    
    # Title at top
    fig.suptitle('The Reverse Prism Hypothesis: Dimensional Dispersion in Consciousness', 
                fontsize=20, fontweight='bold', y=0.96)
    
    plt.tight_layout(rect=[0, 0.15, 1, 0.93])
    return fig


def main():
    """Generate all publication figures"""
    
    print("\n" + "="*70)
    print("PUBLICATION FIGURES GENERATOR - MULTI-SIZE VERSION")
    print("="*70 + "\n")
    
    # Load data
    data = load_multisize_data()
    if data is None:
        return
    
    summary_data, grid_data = data
    
    # Create output directory
    output_dir = Path(__file__).parent / "publication_figures"
    output_dir.mkdir(exist_ok=True)
    
    print("Generating figures...\n")
    
    figures = [
        ("Figure_1_Conceptual_Overview", generate_figure_1_conceptual()),
        ("Figure_2_Loss_Distribution", generate_figure_2_distribution(grid_data)),
        ("Figure_3_Rule_Independence", generate_figure_3_rule_independence(summary_data)),
        ("Figure_4_Grid_Robustness", generate_figure_4_grid_robustness(summary_data)),
        ("Figure_5_Phi_Components", generate_figure_5_phi_components(grid_data)),
        ("Figure_6_Visual_Example", generate_figure_6_visual_example(grid_data)),
        ("Figure_7_Reverse_Prism", generate_figure_7_reverse_prism())
    ]
    
    for name, fig in figures:
        # Save PNG
        png_path = output_dir / f"{name}.png"
        fig.savefig(png_path, dpi=300, bbox_inches='tight')
        
        # Save PDF
        pdf_path = output_dir / f"{name}.pdf"
        fig.savefig(pdf_path, format='pdf', bbox_inches='tight')
        
        print(f"✓ Saved: {name}.png/pdf")
        
        plt.close(fig)
    
    print("\n" + "="*70)
    print("✓ ALL 7 FIGURES GENERATED")
    print("="*70)
    print(f"Location: {output_dir}/")
    print("\nGenerated files:")
    print("  - 7 PNG files (high resolution)")
    print("  - 7 PDF files (vector graphics)")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
