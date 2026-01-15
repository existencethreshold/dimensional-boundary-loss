"""
CRITICAL VALIDATION TEST 3: METRIC SANITY CHECK
===============================================

Tests if Φ metric behaves correctly on edge cases.

Edge cases:
1. All dead cells → Φ should be ~0 (no information)
2. All alive cells → Φ should be ~0 (no information)
3. Checkerboard → Φ should be high (maximum heterogeneity)
4. Random pattern → Φ should be moderate

Author: Nathan M. Thornhill
Date: January 13, 2026
"""

import numpy as np
import sys
from pathlib import Path
import json
from datetime import datetime

# Import from parent directory
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from validate_dimensional_cascade_unified import PhiCalculator


def test_edge_cases():
    """Test Φ metric on edge cases"""
    print("=" * 70)
    print("METRIC SANITY CHECK: EDGE CASES")
    print("=" * 70)
    print()
    
    phi_calc = PhiCalculator()
    results = {}
    
    # Test 1: All Dead
    print("Test 1: All Dead (should be ~0)")
    grid_dead = np.zeros((20, 20), dtype=int)
    phi, R, S, D = phi_calc.calculate_phi(grid_dead)
    print(f"  Φ = {phi:.4f} (R={R:.4f}, S={S:.4f}, D={D:.4f})")
    results['all_dead'] = {'phi': float(phi), 'R': float(R), 'S': float(S), 'D': float(D)}
    assert phi == 0.0, "All dead should have Φ=0"
    print("  ✓ PASSED")
    print()
    
    # Test 2: All Alive
    print("Test 2: All Alive (should be ~0)")
    grid_alive = np.ones((20, 20), dtype=int)
    phi, R, S, D = phi_calc.calculate_phi(grid_alive)
    print(f"  Φ = {phi:.4f} (R={R:.4f}, S={S:.4f}, D={D:.4f})")
    results['all_alive'] = {'phi': float(phi), 'R': float(R), 'S': float(S), 'D': float(D)}
    assert phi == 0.0, "All alive should have Φ=0"
    print("  ✓ PASSED")
    print()
    
    # Test 3: Checkerboard
    print("Test 3: Checkerboard (should be high)")
    grid_checker = np.zeros((20, 20), dtype=int)
    grid_checker[::2, ::2] = 1  # Even rows, even cols
    grid_checker[1::2, 1::2] = 1  # Odd rows, odd cols
    phi, R, S, D = phi_calc.calculate_phi(grid_checker)
    print(f"  Φ = {phi:.4f} (R={R:.4f}, S={S:.4f}, D={D:.4f})")
    results['checkerboard'] = {'phi': float(phi), 'R': float(R), 'S': float(S), 'D': float(D)}
    assert phi > 1.0, "Checkerboard should have high Φ"
    print("  ✓ PASSED")
    print()
    
    # Test 4: Random Pattern
    print("Test 4: Random Pattern (should be moderate)")
    np.random.seed(42)
    grid_random = np.random.choice([0, 1], size=(20, 20), p=[0.5, 0.5])
    phi, R, S, D = phi_calc.calculate_phi(grid_random)
    print(f"  Φ = {phi:.4f} (R={R:.4f}, S={S:.4f}, D={D:.4f})")
    results['random'] = {'phi': float(phi), 'R': float(R), 'S': float(S), 'D': float(D)}
    assert 0.5 < phi < 2.0, "Random should have moderate Φ"
    print("  ✓ PASSED")
    print()
    
    # Test 5: Single Cell
    print("Test 5: Single Cell (should be low)")
    grid_single = np.zeros((20, 20), dtype=int)
    grid_single[10, 10] = 1
    phi, R, S, D = phi_calc.calculate_phi(grid_single)
    print(f"  Φ = {phi:.4f} (R={R:.4f}, S={S:.4f}, D={D:.4f})")
    results['single_cell'] = {'phi': float(phi), 'R': float(R), 'S': float(S), 'D': float(D)}
    assert phi < 0.5, "Single cell should have low Φ"
    print("  ✓ PASSED")
    print()
    
    print("=" * 70)
    print("ALL EDGE CASES PASSED ✓")
    print("=" * 70)
    print()
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output = {
        'metadata': {
            'test': 'metric_sanity_check',
            'timestamp': timestamp
        },
        'results': results,
        'status': 'PASSED'
    }
    
    # Save to tests directory
    filename = Path(__file__).parent / f'metric_sanity_check_{timestamp}.json'
    
    with open(filename, 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"Results saved to: {filename}")
    print("=" * 70)
    
    return results


if __name__ == "__main__":
    test_edge_cases()
