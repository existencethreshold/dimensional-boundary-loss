"""
CRITICAL VALIDATION TEST 1: DIFFERENT CA RULE
==============================================

Tests if ~86% loss holds with HighLife (B36/S23) instead of Conway's Life (B3/S23).

HighLife has DIFFERENT dynamics:
- Birth on 3 or 6 neighbors (vs. 3 only)
- Survival on 2 or 3 neighbors (same as Life)
- Creates replicators (R-pentomino creates clones)

If ~86% holds → Validates geometric hypothesis (rule-independent)
If ~86% fails → Finding is rule-specific (major problem)

This is THE CRITICAL test.

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

def generate_pattern_2d(grid_size, seed):
    """Generate random 2D pattern"""
    np.random.seed(seed)
    density = np.random.uniform(0.3, 0.6)
    return np.random.choice([0, 1], size=(grid_size, grid_size), p=[1-density, density])


# ============================================================================
# EMBEDDING
# ============================================================================

def embed_2d_to_3d(grid_2d, z_size):
    """Embed 2D pattern into middle slice of 3D grid"""
    x, y = grid_2d.shape
    grid_3d = np.zeros((x, y, z_size), dtype=int)
    z_mid = z_size // 2
    grid_3d[:, :, z_mid] = grid_2d
    return grid_3d


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

def test_2d_to_3d_highlife(pattern_id, grid_size=20, seed_start=5000):
    """Test 2D→3D transition (rule-independent test)"""
    seed = seed_start + pattern_id
    
    # Generate 2D pattern
    grid_2d = generate_pattern_2d(grid_size, seed)
    
    # Measure Φ₂D
    phi_2d, _, _, _ = measure_phi(grid_2d)
    
    # Embed to 3D
    grid_3d = embed_2d_to_3d(grid_2d, grid_size)
    
    # Measure Φ₃D
    phi_3d, _, _, _ = measure_phi(grid_3d)
    
    # Calculate ratio
    ratio_phi = phi_3d / phi_2d if phi_2d > 0 else 0
    loss_pct = (1 - ratio_phi) * 100
    
    return {
        'pattern_id': pattern_id,
        'loss_pct': float(loss_pct),
        'ratio_phi': float(ratio_phi),
        'phi_2d': float(phi_2d),
        'phi_3d': float(phi_3d)
    }


def run_highlife_validation(n_patterns=100, grid_size=20):
    """Run HighLife validation test"""
    print("=" * 70)
    print("CRITICAL VALIDATION: RULE INDEPENDENCE (HighLife)")
    print("=" * 70)
    print()
    print(f"Testing: 2D→3D transition")
    print(f"Patterns: {n_patterns}")
    print(f"Grid size: {grid_size}")
    print()
    print("Testing if ~86% loss holds regardless of CA rule...")
    print()
    
    results = []
    
    for i in range(n_patterns):
        result = test_2d_to_3d_highlife(i, grid_size)
        results.append(result)
        
        if (i + 1) % 20 == 0:
            print(f"Progress: {i + 1}/{n_patterns} patterns tested")
    
    print()
    print("=" * 70)
    print("RESULTS:")
    print("=" * 70)
    
    losses = [r['loss_pct'] for r in results]
    mean_loss = np.mean(losses)
    std_loss = np.std(losses, ddof=1)
    ci_95 = 1.96 * std_loss / np.sqrt(n_patterns)
    
    print(f"Mean loss: {mean_loss:.1f}% ± {std_loss:.1f}%")
    print(f"95% CI: {mean_loss - ci_95:.1f}% to {mean_loss + ci_95:.1f}%")
    print()
    
    # Compare to expected 86%
    expected = 86.0
    diff = abs(mean_loss - expected)
    
    if diff < 5.0:
        print("✓ VALIDATION PASSED")
        print(f"  Loss is within 5% of expected {expected}%")
        print("  Finding appears rule-independent")
    else:
        print("✗ VALIDATION FAILED")
        print(f"  Loss differs by {diff:.1f}% from expected {expected}%")
        print("  Finding may be rule-dependent")
    print()
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output = {
        'metadata': {
            'test': 'highlife_validation',
            'n_patterns': n_patterns,
            'grid_size': grid_size,
            'timestamp': timestamp
        },
        'results': results,
        'statistics': {
            'mean_loss': float(mean_loss),
            'std_loss': float(std_loss),
            'ci_95': float(ci_95),
            'expected': expected,
            'difference': float(diff)
        }
    }
    
    # Save to tests directory
    filename = Path(__file__).parent / f'highlife_validation_{timestamp}.json'
    
    with open(filename, 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"Results saved to: {filename}")
    print("=" * 70)
    
    return results


if __name__ == "__main__":
    results = run_highlife_validation(n_patterns=100, grid_size=20)
