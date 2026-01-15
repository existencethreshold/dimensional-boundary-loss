# Methodology

Complete methodology for "Universal Information Loss at Dimensional Boundaries"

## Overview

We measure information loss when embedding discrete patterns from dimension N to dimension N+1 using a novel metric Φ that quantifies pattern persistence. Grid size robustness is validated across multiple spatial scales.

## The Φ (Phi) Metric

### Definition

```
Φ = R·S + D

Components:
  R = Processing rate (ratio of active cells)
  S = Spatial integration (pattern connectivity)
  D = Disorder (Shannon entropy)
```

### Component Calculations

**R (Processing):**
```
R = n_active / n_total

Where:
  n_active = number of "alive" cells (state=1)
  n_total = total number of cells in grid
```

**S (Integration):**
```
S = n_transitions / n_edges

Where:
  n_transitions = count of adjacent cells with different states
  n_edges = total number of adjacent cell pairs
```

For an N-dimensional grid:
- Each cell has 2N neighbors (Moore neighborhood minus center)
- We count transitions along each axis independently

**D (Disorder - Shannon Entropy):**
```
D = -Σ p_i × log₂(p_i)

Where:
  p_alive = n_active / n_total
  p_dead = 1 - p_alive
  
D = -(p_alive × log₂(p_alive) + p_dead × log₂(p_dead))
```

### Rationale

**Why R·S + D?**

- **R·S** captures active **processing × integration**
  - High R + High S = many active, well-connected cells
  - Low R or S = sparse or isolated activity
  
- **D** captures state **uncertainty/complexity**
  - High D = unpredictable, complex patterns
  - Low D = uniform, simple patterns

- **Sum (not product):** Allows R·S and D to contribute independently
  - Processing and disorder are distinct information sources
  - Additive combination prevents zero-inflation

### Interpretation

- **High Φ (>0.5):** Active, integrated, complex pattern
- **Low Φ (<0.2):** Sparse, isolated, simple pattern
- **Zero Φ:** All dead or all alive (no information)

## Embedding Procedure

### 1D → 2D Embedding

```python
# Original 1D pattern (size N)
pattern_1d = [0, 1, 1, 0, 1, ...]

# Create 2D grid (size N×N)
pattern_2d = np.zeros((N, N))

# Place 1D pattern in middle row
pattern_2d[N//2, :] = pattern_1d
```

**Result:** 1D pattern occupies 1/N of 2D space

### 2D → 3D Embedding

```python
# Original 2D pattern (size N×N)
pattern_2d = [[0,1], [1,0]]

# Create 3D grid (size N×N×N)
pattern_3d = np.zeros((N, N, N))

# Place 2D pattern in middle slice
pattern_3d[:, :, N//2] = pattern_2d
```

**Result:** 2D pattern occupies 1/N of 3D space

### 3D → 4D Embedding

```python
# Original 3D pattern (size N×N×N)
pattern_3d = [[[...]]]

# Create 4D grid (size N×N×N×N)
pattern_4d = np.zeros((N, N, N, N))

# Place 3D pattern in middle hyperslice
pattern_4d[:, :, :, N//2] = pattern_3d
```

**Result:** 3D pattern occupies 1/N of 4D space

### General Rule

For dimension D→D+1:
1. Create grid of size N^(D+1)
2. Place D-dimensional pattern in middle "slice" along new axis
3. All other cells remain dead (state=0)

## Pattern Generation

### Random Patterns

```python
import numpy as np

def generate_pattern(dimension, size, seed):
    """Generate random binary pattern"""
    rng = np.random.RandomState(seed)
    
    if dimension == 1:
        return rng.randint(0, 2, size=size)
    elif dimension == 2:
        return rng.randint(0, 2, size=(size, size))
    elif dimension == 3:
        return rng.randint(0, 2, size=(size, size, size))
```

**Properties:**
- Binary states: 0 (dead) or 1 (alive)
- Uniform distribution: P(alive) = P(dead) = 0.5
- Independent: Each pattern uses different random seed

**Justification:**
- Tests **geometric effect** (not specific pattern features)
- Large sample size averages out pattern-specific effects
- Matches theoretical expectation (random → random)

## Experimental Design

### Main Validation (Multi-Size Grid Robustness)

```
Grid sizes tested: N ∈ {15, 17, 20, 23, 25}
Patterns per grid size per transition: 100
Total patterns: 100 patterns × 5 grid sizes × 3 transitions = 1,500

Seeds (consistent across grid sizes):
  1D→2D: seeds 100-199
  2D→3D: seeds 1000-1099
  3D→4D: seeds 3000-3099
```

**Rationale for multi-size testing:**
- Validates scale-independence of 86% finding
- Tests robustness across different spatial resolutions
- Characterizes finite-size effects
- Grid sizes span computationally feasible range (15³=3,375 to 25⁴=390,625 cells)

### Measurements

For each pattern at each grid size:
1. Generate pattern in dimension D
2. Measure Φ_D (native dimension)
3. Embed to dimension D+1
4. Measure Φ_(D+1) (embedded dimension)
5. Calculate loss: (1 - Φ_(D+1)/Φ_D) × 100%

### Data Collection

**Recorded for each pattern:**
- `pattern_id`: 0-99
- `grid_size`: 15, 17, 20, 23, or 25
- `phi_lower`: Φ in native dimension
- `phi_higher`: Φ in embedded dimension
- `ratio_phi`: Φ_higher / Φ_lower
- `loss_pct`: (1 - ratio) × 100
- `R_lower`, `R_higher`: Processing rates
- `S_lower`, `S_higher`: Integration rates
- `D_lower`, `D_higher`: Disorder values
- `alive_cells_lower`, `alive_cells_higher`: Cell counts

## Statistical Analysis

### Central Tendency

```python
mean_loss = np.mean(losses)
median_loss = np.median(losses)
std_loss = np.std(losses, ddof=1)  # Sample std dev
sem_loss = std_loss / np.sqrt(N)    # Standard error
```

### Confidence Intervals (95%)

```python
from scipy import stats

ci_95 = stats.t.interval(
    0.95,
    df=N-1,
    loc=mean_loss,
    scale=sem_loss
)
```

### Consistency Metric

```python
# Coefficient of variation (CV)
cv_pct = (std_loss / mean_loss) * 100

# CV ~3% indicates consistent effect with expected finite-size variation
```

### Multi-Size Analysis

```python
# For each transition, calculate mean loss across grid sizes
for transition in ['1D→2D', '2D→3D', '3D→4D']:
    size_means = []
    for size in [15, 17, 20, 23, 25]:
        losses_at_size = get_losses(transition, size)
        size_means.append(np.mean(losses_at_size))
    
    overall_mean = np.mean(size_means)
    cv_across_sizes = np.std(size_means) / overall_mean * 100
    
# CV <3% across sizes confirms scale-independence
```

### Transition Comparison

```python
# Compare mean loss across transitions
losses_by_transition = {
    '1D→2D': [all loss values across all sizes],
    '2D→3D': [all loss values across all sizes],
    '3D→4D': [all loss values across all sizes]
}

overall_mean = np.mean([np.mean(l) for l in losses_by_transition.values()])
overall_std = np.std([np.mean(l) for l in losses_by_transition.values()])

# Low std (<0.5%) indicates universal effect
```

## Robustness Tests

### Test 1: Grid Size Sensitivity (PRIMARY VALIDATION)

**Question:** Does loss change with grid size?

**Method:**
```python
sizes = [15, 17, 20, 23, 25]

for size in sizes:
    for transition in ['1D→2D', '2D→3D', '3D→4D']:
        # Run N=100 patterns per size per transition
        losses = measure_losses(size, transition)
        mean_loss = np.mean(losses)
        std_loss = np.std(losses)
```

**Results:**
- Mean loss across all sizes: 86.0% ± 2.4%
- Range: 82.5% - 88.6%
- Coefficient of variation: 2.8%

**Interpretation:** 
- ~86% loss holds across all tested grid sizes
- Small variation (CV = 2.8%) consistent with finite-size effects
- Finding is **scale-independent** within tested range

### Test 2: Rule Independence

**Question:** Does specific CA rule matter?

```python
rules = {
    'Conway': 'B3/S23',
    'HighLife': 'B36/S23'
}

for rule_name, rule in rules.items():
    # Run N=100 patterns
    # Measure mean loss

# Expected: Difference <1%
```

**Interpretation:** If similar, effect is **geometric** not **dynamic**

### Test 3: Metric Validation

**Question:** Does Φ metric behave correctly?

```python
edge_cases = {
    'all_dead': np.zeros((20, 20)),
    'all_alive': np.ones((20, 20)),
    'single_cell': pattern with one alive cell,
    'checkerboard': alternating 0/1 pattern
}

for case, pattern in edge_cases.items():
    phi = calculate_phi(pattern)
    # Verify expected behavior
```

**Expected:**
- All dead: Φ ≈ 0
- All alive: Φ ≈ 0
- Single cell: Φ ≈ low (sparse)
- Checkerboard: Φ ≈ high (complex)

## Limitations

### Known Limitations

1. **Discrete systems only:** Continuous systems may behave differently
2. **Static embedding:** Does not account for temporal dynamics
3. **Binary states:** Multi-state systems not tested
4. **Specific embedding:** Middle-placement; other embeddings not tested
5. **Computational:** High dimensions (5D+) require significant resources
6. **Finite-size effects:** Small grids (N<15) may show larger variation

### Assumptions

1. **Random patterns representative:** Tests geometric effect, not specific patterns
2. **Sample size sufficient:** 100 patterns per grid size per transition provides statistical power
3. **Grid size range adequate:** Range 15-25 balances computation with statistical stability
4. **Φ metric valid:** Captures relevant information properties

### Future Work

- Test continuous-valued patterns
- Investigate alternative embedding strategies  
- Extend to 5D, 6D (computational challenge)
- Test biological/physical systems
- Develop analytical model
- Characterize finite-size effects for N<15

## Reproducibility

### Exact Replication

```bash
# Run multi-size validation (same seeds, same parameters)
python validate_dimensional_cascade_multisize.py

# Compare output to published data
# Files: validation_results_multisize/dimensional_cascade_N100_grid*.json
#        validation_results_multisize/multisize_summary_*.json
```

**Expected:** 
- Mean loss within ±1% of published values per grid size
- Overall mean 86.0% ± 2.4%
- CV across sizes ~2.8%

### Statistical Replication

```bash
# Run with different seeds (not included in standard script)
# Modify script to use seeds 200-299, 2000-2099, 4000-4099

# Compare statistics (not exact values)
```

**Expected:** Mean loss within 82-90% range across grid sizes, CV <5%

## Code Availability

All code, data, and documentation available at:
- **GitHub:** https://github.com/existencethreshold/dimensional-boundary-loss
- **Zenodo:** https://doi.org/10.5281/zenodo.18238486

**License:** MIT (free to use with attribution)

---

**Last Updated:** January 2026  
**Corresponding Author:** Nathan M. Thornhill (existencethreshold@gmail.com)
