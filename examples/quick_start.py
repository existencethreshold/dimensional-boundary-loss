"""
QUICK START EXAMPLE: 1D→2D Information Loss

Demonstrates basic usage of the dimensional cascade validation.
Shows how to measure information loss for a single pattern.

Author: Nathan M. Thornhill
"""

import numpy as np
import sys
from pathlib import Path

# Simple Phi calculator (inline for clarity)
def calculate_phi(pattern):
    """Calculate Φ = R·S + D for a pattern"""
    
    flat = pattern.flatten()
    n_cells = len(flat)
    alive_cells = np.sum(flat)
    
    # Edge case: all dead or all alive
    if alive_cells == 0 or alive_cells == n_cells:
        return (0.0, 0.0, 0.0, 0.0)
    
    # R: Processing (active cells ratio)
    R = alive_cells / n_cells
    
    # S: Integration (transitions between states)
    ndim = pattern.ndim
    transitions = 0
    total_edges = 0
    
    for axis in range(ndim):
        shifted = np.roll(pattern, 1, axis=axis)
        transitions += np.sum(pattern != shifted)
        total_edges += pattern.size
    
    S = transitions / total_edges if total_edges > 0 else 0.0
    
    # D: Disorder (Shannon entropy)
    p_alive = alive_cells / n_cells
    p_dead = 1 - p_alive
    D = -(p_alive * np.log2(p_alive) + p_dead * np.log2(p_dead))
    
    # Φ = R·S + D
    phi = R * S + D
    
    return (phi, R, S, D)


def main():
    """Demonstrate 1D→2D information loss"""
    
    print("="*70)
    print("QUICK START: 1D→2D INFORMATION LOSS")
    print("="*70)
    print()
    
    # Parameters
    grid_size = 20
    seed = 42
    
    print(f"Configuration:")
    print(f"  Grid size: {grid_size}")
    print(f"  Random seed: {seed}")
    print()
    
    # Generate 1D pattern
    rng = np.random.RandomState(seed)
    pattern_1d = rng.randint(0, 2, size=grid_size).astype(int)
    
    print("1D Pattern:")
    print(''.join(['█' if x else '·' for x in pattern_1d]))
    print(f"Alive cells: {np.sum(pattern_1d)}/{grid_size}")
    print()
    
    # Measure Φ in 1D
    phi_1d, R_1d, S_1d, D_1d = calculate_phi(pattern_1d)
    
    print("1D Measurement:")
    print(f"  Φ = {phi_1d:.4f}")
    print(f"  R (Processing) = {R_1d:.4f}")
    print(f"  S (Integration) = {S_1d:.4f}")
    print(f"  D (Disorder) = {D_1d:.4f}")
    print()
    
    # Embed to 2D (middle row)
    pattern_2d = np.zeros((grid_size, grid_size), dtype=int)
    pattern_2d[grid_size // 2, :] = pattern_1d
    
    print("2D Embedding:")
    print(f"  Grid: {grid_size}×{grid_size}")
    print(f"  Pattern in middle row (row {grid_size//2})")
    print(f"  Alive cells: {np.sum(pattern_2d)}/{grid_size**2}")
    print()
    
    # Measure Φ in 2D
    phi_2d, R_2d, S_2d, D_2d = calculate_phi(pattern_2d)
    
    print("2D Measurement:")
    print(f"  Φ = {phi_2d:.4f}")
    print(f"  R (Processing) = {R_2d:.4f}")
    print(f"  S (Integration) = {S_2d:.4f}")
    print(f"  D (Disorder) = {D_2d:.4f}")
    print()
    
    # Calculate loss
    ratio = phi_2d / phi_1d if phi_1d > 0 else 0
    loss_pct = (1 - ratio) * 100
    
    print("="*70)
    print("RESULT")
    print("="*70)
    print(f"Information retained: {ratio*100:.2f}%")
    print(f"Information lost: {loss_pct:.2f}%")
    print()
    print("Expected range: 80-92% (pattern-dependent)")
    print("Expected mean: ~86% (across many patterns)")
    print()
    
    if 80 < loss_pct < 92:
        print("✓ Result within expected range")
    else:
        print("⚠ Result outside typical range (unusual pattern)")
    
    print()
    print("="*70)
    print("INTERPRETATION")
    print("="*70)
    print()
    print("The ~86% loss comes from geometric dilution:")
    print(f"  • 1D pattern: {np.sum(pattern_1d)} cells in {grid_size} positions")
    print(f"  • 2D embedding: same {np.sum(pattern_2d)} cells in {grid_size**2} positions")
    print(f"  • Spatial density decreased by factor of {grid_size}")
    print()
    print("This affects:")
    print("  R (Processing): More dead cells reduces active ratio")
    print("  S (Integration): Pattern more isolated in larger space")
    print("  D (Disorder): Remains similar (pattern entropy unchanged)")
    print()
    print("Result: Φ drops by ~86%")
    print()
    print("="*70)
    print("NEXT STEPS")
    print("="*70)
    print()
    print("1. Full validation (1,500 patterns across 5 grid sizes):")
    print("   python validate_dimensional_cascade_multisize.py")
    print()
    print("2. Generate publication figures:")
    print("   python generate_publication_figures.py")
    print()
    print("3. See docs/METHODOLOGY.md for detailed explanation")
    print()


if __name__ == "__main__":
    main()
