"""
CRITICAL VALIDATION TEST 2: GRID SIZE SENSITIVITY
==================================================

Tests if ~86% loss depends on grid_size=20.

Tests sizes: [15, 20, 25]
- If loss stays ~86% → Size-independent (robust finding)
- If loss changes → Size artifact (major problem)

Author: Nathan M. Thornhill
Date: January 13, 2026
"""

import numpy as np
import sys
from pathlib import Path
import json
from datetime import datetime
from scipy import stats

# Import from parent directory
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from validate_dimensional_cascade_unified import PhiCalculator


# ============================================================================
# PATTERN GENERATION
# ============================================================================

def generate_pattern_1d(grid_size, seed):
    """Generate random 1D pattern"""
    np.random.seed(seed)
    density = np.random.uniform(0.3, 0.6)
    return np.random.choice([0, 1], size=grid_size, p=[1-density, density])


# ============================================================================
# EMBEDDING
# ============================================================================

def embed_1d_to_2d(grid_1d, y_size):
    """Embed 1D pattern into middle row of 2D grid"""
    x = grid_1d.shape[0]
    grid_2d = np.zeros((x, y_size), dtype=int)
    y_mid = y_size // 2
    grid_2d[:, y_mid] = grid_1d
    return grid_2d


# ============================================================================
# PHI MEASUREMENT
# ============================================================================

def measure_phi(grid):
    """Measure Φ using PhiCalculator"""
    phi_calc = PhiCalculator()
    phi, R, S, D = phi_calc.calculate_phi(grid)
    return phi, R, S, D


# ============================================================================
# MAIN TEST
# ============================================================================

def test_1d_to_2d_size(pattern_id, grid_size, seed_start=6000):
    """Test 1D→2D with specific grid size"""
    seed = seed_start + pattern_id
    
    # Generate 1D pattern
    grid_1d = generate_pattern_1d(grid_size, seed)
    
    # Measure Φ₁D
    phi_1d, _, _, _ = measure_phi(grid_1d)
    
    # Embed to 2D
    grid_2d = embed_1d_to_2d(grid_1d, grid_size)
    
    # Measure Φ₂D
    phi_2d, _, _, _ = measure_phi(grid_2d)
    
    # Calculate ratio
    ratio_phi = phi_2d / phi_1d if phi_1d > 0 else 0
    loss_pct = (1 - ratio_phi) * 100
    
    return {
        'pattern_id': pattern_id,
        'grid_size': grid_size,
        'loss_pct': float(loss_pct),
        'ratio_phi': float(ratio_phi),
        'phi_1d': float(phi_1d),
        'phi_2d': float(phi_2d)
    }


def run_grid_size_validation(grid_sizes=[15, 20, 25], n_per_size=20):
    """Test multiple grid sizes"""
    print("=" * 70)
    print("CRITICAL VALIDATION: GRID SIZE SENSITIVITY")
    print("=" * 70)
    print()
    print(f"Testing sizes: {grid_sizes}")
    print(f"Patterns per size: {n_per_size}")
    print()
    
    all_results = {}
    
    for grid_size in grid_sizes:
        print(f"Testing grid size {grid_size}...")
        results = []
        
        for i in range(n_per_size):
            result = test_1d_to_2d_size(i, grid_size)
            results.append(result)
        
        all_results[grid_size] = results
        
        # Quick stats
        losses = [r['loss_pct'] for r in results]
        mean_loss = np.mean(losses)
        print(f"  → Mean loss: {mean_loss:.1f}%")
    
    print()
    print("=" * 70)
    print("GRID SIZE COMPARISON:")
    print("=" * 70)
    
    size_stats = {}
    for grid_size in grid_sizes:
        losses = [r['loss_pct'] for r in all_results[grid_size]]
        mean_loss = np.mean(losses)
        std_loss = np.std(losses, ddof=1)
        size_stats[grid_size] = {'mean': mean_loss, 'std': std_loss}
        
        print(f"Size {grid_size:2d}: {mean_loss:5.1f}% ± {std_loss:4.1f}%")
    
    print()
    
    # Check consistency
    means = [size_stats[s]['mean'] for s in grid_sizes]
    mean_of_means = np.mean(means)
    std_of_means = np.std(means, ddof=1)
    
    print(f"Overall mean: {mean_of_means:.1f}%")
    print(f"Variation across sizes: {std_of_means:.1f}%")
    print()
    
    if std_of_means < 5.0:
        print("✓ VALIDATION PASSED")
        print("  Loss percentage is consistent across grid sizes")
        print("  Finding is size-independent")
    else:
        print("✗ VALIDATION FAILED")
        print("  Loss percentage varies significantly with grid size")
        print("  Finding may be size-dependent artifact")
    print()
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output = {
        'metadata': {
            'test': 'grid_size_sensitivity',
            'grid_sizes': grid_sizes,
            'n_per_size': n_per_size,
            'timestamp': timestamp
        },
        'results': all_results,
        'statistics': {
            size: size_stats[size] for size in grid_sizes
        },
        'summary': {
            'overall_mean': float(mean_of_means),
            'std_across_sizes': float(std_of_means)
        }
    }
    
    # Save to tests directory (since we're running from there)
    filename = Path(__file__).parent / f'grid_size_validation_{timestamp}.json'
    
    with open(filename, 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"Results saved to: {filename}")
    print("=" * 70)
    
    return all_results


if __name__ == "__main__":
    results = run_grid_size_validation(
        grid_sizes=[15, 17, 20, 23, 25],
        n_per_size=20
    )
