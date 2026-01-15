"""
UNIFIED DIMENSIONAL CASCADE VALIDATION - MULTI-GRID SIZE
Comprehensive validation of information loss across dimensional boundaries
Tests robustness across multiple grid sizes: {15, 17, 20, 23, 25}

COMPLETELY SELF-CONTAINED - NO EXTERNAL DEPENDENCIES
Only requires: numpy

Tests: 1D→2D, 2D→3D, 3D→4D (100 patterns each, 5 grid sizes)
Runtime: ~2.5 hours total
Output: JSON files for each grid size + combined summary

Author: Nathan M. Thornhill
Date: January 13, 2026
"""

import numpy as np
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Tuple, List
import time


# ============================================================================
# PHI METRIC CALCULATOR
# ============================================================================

class PhiCalculator:
    """
    Calculate Φ = R·S + D where:
    - R = Processing (ratio of active cells)
    - S = Integration (spatial pattern complexity)
    - D = Disorder (Shannon entropy)
    """
    
    def calculate_phi(self, pattern: np.ndarray) -> Tuple[float, float, float, float]:
        """Calculate Φ metric and components"""
        
        flat = pattern.flatten()
        n_cells = len(flat)
        alive_cells = np.sum(flat)
        
        # Edge case: all dead or all alive
        if alive_cells == 0 or alive_cells == n_cells:
            return (0.0, 0.0, 0.0, 0.0)
        
        # R: Processing (proportion of active cells)
        R = alive_cells / n_cells
        
        # S: Integration (spatial transitions / edges)
        S = self._calculate_integration(pattern)
        
        # D: Disorder (Shannon entropy)
        p_alive = alive_cells / n_cells
        p_dead = 1 - p_alive
        D = -(p_alive * np.log2(p_alive) + p_dead * np.log2(p_dead))
        
        # Φ = R·S + D
        phi = R * S + D
        
        return (phi, R, S, D)
    
    def _calculate_integration(self, pattern: np.ndarray) -> float:
        """Count transitions between different states (edges)"""
        
        ndim = pattern.ndim
        transitions = 0
        total_edges = 0
        
        # Check each dimension
        for axis in range(ndim):
            # Shift pattern along this axis
            shifted = np.roll(pattern, 1, axis=axis)
            # Count where neighbors differ
            transitions += np.sum(pattern != shifted)
            total_edges += pattern.size
        
        # Normalize
        S = transitions / total_edges if total_edges > 0 else 0.0
        return S


# ============================================================================
# DIMENSIONAL CASCADE VALIDATOR
# ============================================================================

class DimensionalCascadeValidator:
    """Validate information loss across all dimensional transitions"""
    
    def __init__(self, n_patterns: int = 100, grid_size: int = 20):
        self.n_patterns = n_patterns
        self.grid_size = grid_size
        self.phi_calc = PhiCalculator()
    
    def generate_1d_pattern(self, seed: int) -> np.ndarray:
        """Generate random 1D binary pattern"""
        rng = np.random.RandomState(seed)
        return rng.randint(0, 2, size=self.grid_size).astype(int)
    
    def generate_2d_pattern(self, seed: int) -> np.ndarray:
        """Generate random 2D binary pattern"""
        rng = np.random.RandomState(seed)
        return rng.randint(0, 2, size=(self.grid_size, self.grid_size)).astype(int)
    
    def generate_3d_pattern(self, seed: int) -> np.ndarray:
        """Generate random 3D binary pattern"""
        rng = np.random.RandomState(seed)
        return rng.randint(0, 2, size=(self.grid_size, self.grid_size, self.grid_size)).astype(int)
    
    def test_1d_to_2d(self, pattern_id: int, seed: int) -> Dict:
        """Test 1D pattern embedded in 2D space"""
        
        # Generate 1D pattern
        pattern_1d = self.generate_1d_pattern(seed)
        
        # Measure in native 1D
        phi_1d, R_1d, S_1d, D_1d = self.phi_calc.calculate_phi(pattern_1d)
        
        # Embed in 2D (middle row)
        pattern_2d = np.zeros((self.grid_size, self.grid_size), dtype=int)
        pattern_2d[self.grid_size // 2, :] = pattern_1d
        
        # Measure in 2D
        phi_2d, R_2d, S_2d, D_2d = self.phi_calc.calculate_phi(pattern_2d)
        
        # Calculate loss
        ratio = phi_2d / phi_1d if phi_1d > 0 else 0
        loss = (1 - ratio) * 100
        
        return {
            'pattern_id': pattern_id,
            'transition': '1D→2D',
            'phi_lower': float(phi_1d),
            'phi_higher': float(phi_2d),
            'ratio_phi': float(ratio),
            'loss_pct': float(loss),
            'R_lower': float(R_1d),
            'R_higher': float(R_2d),
            'ratio_R': float(R_2d / R_1d if R_1d > 0 else 0),
            'S_lower': float(S_1d),
            'S_higher': float(S_2d),
            'ratio_S': float(S_2d / S_1d if S_1d > 0 else 0),
            'D_lower': float(D_1d),
            'D_higher': float(D_2d),
            'ratio_D': float(D_2d / D_1d if D_1d > 0 else 0),
            'alive_cells_lower': int(np.sum(pattern_1d)),
            'alive_cells_higher': int(np.sum(pattern_2d))
        }
    
    def test_2d_to_3d(self, pattern_id: int, seed: int) -> Dict:
        """Test 2D pattern embedded in 3D space"""
        
        # Generate 2D pattern
        pattern_2d = self.generate_2d_pattern(seed)
        
        # Measure in native 2D
        phi_2d, R_2d, S_2d, D_2d = self.phi_calc.calculate_phi(pattern_2d)
        
        # Embed in 3D (middle slice)
        pattern_3d = np.zeros((self.grid_size, self.grid_size, self.grid_size), dtype=int)
        pattern_3d[:, :, self.grid_size // 2] = pattern_2d
        
        # Measure in 3D
        phi_3d, R_3d, S_3d, D_3d = self.phi_calc.calculate_phi(pattern_3d)
        
        # Calculate loss
        ratio = phi_3d / phi_2d if phi_2d > 0 else 0
        loss = (1 - ratio) * 100
        
        return {
            'pattern_id': pattern_id,
            'transition': '2D→3D',
            'phi_lower': float(phi_2d),
            'phi_higher': float(phi_3d),
            'ratio_phi': float(ratio),
            'loss_pct': float(loss),
            'R_lower': float(R_2d),
            'R_higher': float(R_3d),
            'ratio_R': float(R_3d / R_2d if R_2d > 0 else 0),
            'S_lower': float(S_2d),
            'S_higher': float(S_3d),
            'ratio_S': float(S_3d / S_2d if S_2d > 0 else 0),
            'D_lower': float(D_2d),
            'D_higher': float(D_3d),
            'ratio_D': float(D_3d / D_2d if D_2d > 0 else 0),
            'alive_cells_lower': int(np.sum(pattern_2d)),
            'alive_cells_higher': int(np.sum(pattern_3d))
        }
    
    def test_3d_to_4d(self, pattern_id: int, seed: int) -> Dict:
        """Test 3D pattern embedded in 4D space"""
        
        # Generate 3D pattern
        pattern_3d = self.generate_3d_pattern(seed)
        
        # Measure in native 3D
        phi_3d, R_3d, S_3d, D_3d = self.phi_calc.calculate_phi(pattern_3d)
        
        # Embed in 4D (middle hyperslice)
        pattern_4d = np.zeros(
            (self.grid_size, self.grid_size, self.grid_size, self.grid_size),
            dtype=int
        )
        pattern_4d[:, :, :, self.grid_size // 2] = pattern_3d
        
        # Measure in 4D
        phi_4d, R_4d, S_4d, D_4d = self.phi_calc.calculate_phi(pattern_4d)
        
        # Calculate loss
        ratio = phi_4d / phi_3d if phi_3d > 0 else 0
        loss = (1 - ratio) * 100
        
        return {
            'pattern_id': pattern_id,
            'transition': '3D→4D',
            'phi_lower': float(phi_3d),
            'phi_higher': float(phi_4d),
            'ratio_phi': float(ratio),
            'loss_pct': float(loss),
            'R_lower': float(R_3d),
            'R_higher': float(R_4d),
            'ratio_R': float(R_4d / R_3d if R_3d > 0 else 0),
            'S_lower': float(S_3d),
            'S_higher': float(S_4d),
            'ratio_S': float(S_4d / S_3d if S_3d > 0 else 0),
            'D_lower': float(D_3d),
            'D_higher': float(D_4d),
            'ratio_D': float(D_4d / D_3d if D_3d > 0 else 0),
            'alive_cells_lower': int(np.sum(pattern_3d)),
            'alive_cells_higher': int(np.sum(pattern_4d))
        }
    
    def run_all_tests(self, show_progress: bool = True) -> Dict:
        """Run all dimensional transition tests"""
        
        results = {
            'test_1d_2d': [],
            'test_2d_3d': [],
            'test_3d_4d': []
        }
        
        # 1D→2D
        if show_progress:
            print(f"  Testing 1D→2D (N={self.grid_size})...")
        start = time.time()
        for i in range(self.n_patterns):
            seed = 100 + i
            result = self.test_1d_to_2d(i, seed)
            results['test_1d_2d'].append(result)
            
            if show_progress and (i + 1) % 20 == 0:
                elapsed = time.time() - start
                rate = (i + 1) / elapsed
                remaining = (self.n_patterns - i - 1) / rate
                print(f"    {i + 1}/{self.n_patterns} | ETA: {remaining:.0f}s")
        
        if show_progress:
            print(f"    ✓ Completed in {time.time() - start:.1f}s")
        
        # 2D→3D
        if show_progress:
            print(f"  Testing 2D→3D (N={self.grid_size})...")
        start = time.time()
        for i in range(self.n_patterns):
            seed = 1000 + i
            result = self.test_2d_to_3d(i, seed)
            results['test_2d_3d'].append(result)
            
            if show_progress and (i + 1) % 20 == 0:
                elapsed = time.time() - start
                rate = (i + 1) / elapsed
                remaining = (self.n_patterns - i - 1) / rate
                print(f"    {i + 1}/{self.n_patterns} | ETA: {remaining:.0f}s")
        
        if show_progress:
            print(f"    ✓ Completed in {time.time() - start:.1f}s")
        
        # 3D→4D
        if show_progress:
            print(f"  Testing 3D→4D (N={self.grid_size})...")
        start = time.time()
        for i in range(self.n_patterns):
            seed = 3000 + i
            result = self.test_3d_to_4d(i, seed)
            results['test_3d_4d'].append(result)
            
            if show_progress and (i + 1) % 20 == 0:
                elapsed = time.time() - start
                rate = (i + 1) / elapsed
                remaining = (self.n_patterns - i - 1) / rate
                print(f"    {i + 1}/{self.n_patterns} | ETA: {remaining:.0f}s")
        
        if show_progress:
            print(f"    ✓ Completed in {time.time() - start:.1f}s\n")
        
        return results
    
    def calculate_statistics(self, results: Dict) -> Dict:
        """Calculate statistics for each transition"""
        
        stats = {}
        
        for test_name, test_data in results.items():
            losses = [r['loss_pct'] for r in test_data]
            
            stats[test_name] = {
                'n': len(losses),
                'mean_loss_pct': float(np.mean(losses)),
                'std_loss_pct': float(np.std(losses, ddof=1)),
                'sem_loss_pct': float(np.std(losses, ddof=1) / np.sqrt(len(losses))),
                'min_loss_pct': float(np.min(losses)),
                'max_loss_pct': float(np.max(losses)),
                'median_loss_pct': float(np.median(losses)),
                'q25_loss_pct': float(np.percentile(losses, 25)),
                'q75_loss_pct': float(np.percentile(losses, 75))
            }
        
        return stats
    
    def save_results(self, results: Dict, stats: Dict, output_dir: str, grid_size: int) -> Path:
        """Save results to JSON file"""
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"dimensional_cascade_N{self.n_patterns}_grid{grid_size}_{timestamp}.json"
        filepath = output_path / filename
        
        output = {
            'metadata': {
                'timestamp': datetime.now().isoformat(),
                'test_type': 'UNIFIED_DIMENSIONAL_CASCADE',
                'description': 'Comprehensive validation of information loss at dimensional boundaries',
                'config': {
                    'n_patterns': self.n_patterns,
                    'grid_size': grid_size,
                    'seed_ranges': {
                        '1d_2d': '100-199',
                        '2d_3d': '1000-1099',
                        '3d_4d': '3000-3099'
                    }
                }
            },
            'test_1d_2d': results['test_1d_2d'],
            'test_2d_3d': results['test_2d_3d'],
            'test_3d_4d': results['test_3d_4d'],
            'statistics': stats
        }
        
        with open(filepath, 'w') as f:
            json.dump(output, f, indent=2)
        
        return filepath


# ============================================================================
# MULTI-SIZE RUNNER
# ============================================================================

def run_multisize_validation(
    grid_sizes: List[int],
    n_patterns: int = 100,
    output_dir: str = "validation_results"
):
    """Run validation across multiple grid sizes"""
    
    print(f"\n{'='*70}")
    print("MULTI-SIZE DIMENSIONAL CASCADE VALIDATION")
    print(f"{'='*70}")
    print(f"Grid sizes: {grid_sizes}")
    print(f"Patterns per size: {n_patterns}")
    print(f"Total patterns: {n_patterns * len(grid_sizes) * 3}")
    print(f"Estimated time: ~{len(grid_sizes) * 30} minutes")
    print(f"{'='*70}\n")
    
    all_results = {}
    all_stats = {}
    
    total_start = time.time()
    
    for grid_size in grid_sizes:
        print(f"{'='*70}")
        print(f"GRID SIZE: {grid_size}")
        print(f"{'='*70}\n")
        
        validator = DimensionalCascadeValidator(
            n_patterns=n_patterns,
            grid_size=grid_size
        )
        
        # Run tests
        results = validator.run_all_tests(show_progress=True)
        
        # Calculate statistics
        stats = validator.calculate_statistics(results)
        
        # Save individual results
        filepath = validator.save_results(results, stats, output_dir, grid_size)
        print(f"✓ Saved: {filepath.name}\n")
        
        # Store for summary
        all_results[grid_size] = results
        all_stats[grid_size] = stats
    
    # Create combined summary
    summary = create_multisize_summary(all_stats, grid_sizes, n_patterns)
    
    # Save summary
    summary_path = save_summary(summary, output_dir)
    
    total_time = time.time() - total_start
    
    print(f"\n{'='*70}")
    print("MULTI-SIZE VALIDATION COMPLETE")
    print(f"{'='*70}")
    print(f"Total time: {total_time/60:.1f} minutes")
    print(f"Results saved to: {output_dir}/")
    print(f"Summary: {summary_path.name}")
    print(f"{'='*70}\n")
    
    print_multisize_summary(summary)
    
    return all_results, all_stats, summary


def create_multisize_summary(all_stats: Dict, grid_sizes: List[int], n_patterns: int) -> Dict:
    """Create summary across all grid sizes"""
    
    summary = {
        'metadata': {
            'timestamp': datetime.now().isoformat(),
            'test_type': 'MULTI_SIZE_GRID_SENSITIVITY',
            'grid_sizes': grid_sizes,
            'n_patterns_per_size': n_patterns,
            'total_patterns': n_patterns * len(grid_sizes) * 3
        },
        'results_by_size': {},
        'consistency_analysis': {}
    }
    
    # Organize by grid size
    for size in grid_sizes:
        summary['results_by_size'][f'grid_{size}'] = all_stats[size]
    
    # Analyze consistency across sizes
    for test_name in ['test_1d_2d', 'test_2d_3d', 'test_3d_4d']:
        means = [all_stats[size][test_name]['mean_loss_pct'] for size in grid_sizes]
        stds = [all_stats[size][test_name]['std_loss_pct'] for size in grid_sizes]
        
        summary['consistency_analysis'][test_name] = {
            'mean_across_sizes': float(np.mean(means)),
            'std_across_sizes': float(np.std(means, ddof=1)),
            'min_mean': float(np.min(means)),
            'max_mean': float(np.max(means)),
            'mean_std': float(np.mean(stds)),
            'coefficient_of_variation': float(np.std(means, ddof=1) / np.mean(means) * 100)
        }
    
    return summary


def save_summary(summary: Dict, output_dir: str) -> Path:
    """Save multi-size summary"""
    
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"multisize_summary_{timestamp}.json"
    filepath = output_path / filename
    
    with open(filepath, 'w') as f:
        json.dump(summary, f, indent=2)
    
    return filepath


def print_multisize_summary(summary: Dict):
    """Print summary of multi-size validation"""
    
    print(f"{'='*70}")
    print("GRID SIZE ROBUSTNESS SUMMARY")
    print(f"{'='*70}\n")
    
    for test_name, analysis in summary['consistency_analysis'].items():
        transition = test_name.replace('test_', '').replace('_', '→').upper()
        
        print(f"{transition}:")
        print(f"  Mean across sizes: {analysis['mean_across_sizes']:.2f}%")
        print(f"  Range: {analysis['min_mean']:.2f}% - {analysis['max_mean']:.2f}%")
        print(f"  Variability: ±{analysis['std_across_sizes']:.2f}%")
        print(f"  Coefficient of variation: {analysis['coefficient_of_variation']:.3f}%")
        print()
    
    # Overall finding
    all_means = [a['mean_across_sizes'] for a in summary['consistency_analysis'].values()]
    overall_mean = np.mean(all_means)
    overall_cv = np.std(all_means, ddof=1) / overall_mean * 100
    
    print(f"OVERALL CONSISTENCY:")
    print(f"  Mean loss: ~{overall_mean:.0f}%")
    print(f"  Stability across sizes: CV = {overall_cv:.3f}%")
    print(f"  Finding: Scale-independent ~{overall_mean:.0f}% loss at boundaries")
    print(f"{'='*70}\n")


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Run multi-size grid validation"""
    
    # Configuration
    GRID_SIZES = [15, 17, 20, 23, 25]
    N_PATTERNS = 100
    OUTPUT_DIR = "validation_results_multisize"
    
    # Run validation
    all_results, all_stats, summary = run_multisize_validation(
        grid_sizes=GRID_SIZES,
        n_patterns=N_PATTERNS,
        output_dir=OUTPUT_DIR
    )
    
    print("✓ Ready for paper update and GitHub upload")
    
    return all_results, all_stats, summary


if __name__ == "__main__":
    main()