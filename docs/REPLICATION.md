# Replication Guide

Complete step-by-step instructions to replicate "Universal Information Loss at Dimensional Boundaries"

## Overview

This guide provides three replication pathways:
1. **Quick Verification** (~5 minutes) - Verify concept with single example
2. **Full Replication** (~2.5 hours) - Reproduce published results exactly
3. **Extended Validation** (~3 hours) - Include robustness tests

## Prerequisites

### System Requirements

- **Python:** 3.8 or higher
- **RAM:** 8GB minimum, 16GB recommended (for 4D grids)
- **Disk:** 200MB free space
- **OS:** Windows, macOS, or Linux

### Software Installation

```bash
# Clone repository
git clone https://github.com/existencethreshold/dimensional-boundary-loss
cd dimensional-boundary-loss

# Install dependencies
pip install -r requirements.txt

# Verify installation
python -c "import numpy, scipy, matplotlib; print('✓ All dependencies installed')"
```

## Pathway 1: Quick Verification

**Time:** ~5 minutes  
**Goal:** Verify the concept works

### Step 1: Run Quick Start

```bash
python examples/quick_start.py
```

### Expected Output

```
======================================================================
QUICK START: 1D→2D INFORMATION LOSS
======================================================================

Configuration:
  Grid size: 20
  Random seed: 42

1D Pattern:
·█··█·████·█·█████·█
Alive cells: 13/20

1D Measurement:
  Φ = 1.0123
  R (Processing) = 0.6500
  S (Integration) = 0.5000
  D (Disorder) = 0.9544

2D Embedding:
  Grid: 20×20
  Pattern in middle row (row 10)
  Alive cells: 13/400

2D Measurement:
  Φ = 0.1456
  R (Processing) = 0.0325
  S (Integration) = 0.0975
  D (Disorder) = 0.2256

======================================================================
RESULT
======================================================================
Information retained: 14.38%
Information lost: 85.62%

Expected range: 80-92% (pattern-dependent)
Expected mean: ~86% (across many patterns)

✓ Result within expected range
```

### Interpretation

- **Single pattern:** 85.62% loss
- **Within expected range:** 80-92%
- **Concept verified:** ✓ Loss occurs during embedding

**Next:** Full replication to confirm statistical consistency

## Pathway 2: Full Replication

**Time:** ~2.5 hours  
**Goal:** Reproduce published results exactly

### Step 2: Run Full Multi-Size Validation

```bash
python validate_dimensional_cascade_multisize.py
```

### What It Does

Tests 1,500 patterns total:
- Grid sizes: {15, 17, 20, 23, 25}
- 100 patterns per grid size per transition
- 3 transitions: 1D→2D, 2D→3D, 3D→4D
- Seeds: 100-199 (1D→2D), 1000-1099 (2D→3D), 3000-3099 (3D→4D)

### Progress Output

```
======================================================================
MULTI-SIZE DIMENSIONAL CASCADE VALIDATION
======================================================================
Grid sizes: [15, 17, 20, 23, 25]
Patterns per size: 100
Total patterns: 1,500
Estimated time: ~2.5 hours
======================================================================

======================================================================
GRID SIZE: 15
======================================================================

  Testing 1D→2D (N=15)...
    20/100 | ETA: 90s
    ...
    ✓ Completed in 152.3s

  Testing 2D→3D (N=15)...
    ✓ Completed in 423.8s

  Testing 3D→4D (N=15)...
    ✓ Completed in 947.2s

✓ Saved: dimensional_cascade_N100_grid15_*.json

======================================================================
GRID SIZE: 17
======================================================================
...

[Process repeats for grid sizes 17, 20, 23, 25]

======================================================================
MULTI-SIZE VALIDATION COMPLETE
======================================================================
Total time: 152.4 minutes
Results saved to: validation_results_multisize/
Summary: multisize_summary_*.json
======================================================================

======================================================================
GRID SIZE ROBUSTNESS SUMMARY
======================================================================

1D→2D:
  Mean across sizes: 85.82%
  Range: 82.49% - 88.50%
  Variability: ±2.50%
  Coefficient of variation: 2.917%

2D→3D:
  Mean across sizes: 86.09%
  Range: 82.95% - 88.64%
  Variability: ±2.35%
  Coefficient of variation: 2.728%

3D→4D:
  Mean across sizes: 86.12%
  Range: 83.02% - 88.64%
  Variability: ±2.31%
  Coefficient of variation: 2.688%

OVERALL CONSISTENCY:
  Mean loss: ~86%
  Stability across sizes: CV = 0.189%
  Finding: Scale-independent ~86% loss at boundaries
======================================================================

✓ Ready for paper update and GitHub upload
```

### Verify Results

```bash
# Check output files exist
ls validation_results_multisize/

# Should show:
# dimensional_cascade_N100_grid15_*.json
# dimensional_cascade_N100_grid17_*.json
# dimensional_cascade_N100_grid20_*.json
# dimensional_cascade_N100_grid23_*.json
# dimensional_cascade_N100_grid25_*.json
# multisize_summary_*.json
```

### Compare to Published Data

Open `validation_results_multisize/multisize_summary_*.json` and compare statistics:

| Metric | Your Result | Published | Match? |
|--------|------------|-----------|---------|
| 1D→2D mean | ~85.8% | 85.8% | ✓ |
| 2D→3D mean | ~86.1% | 86.1% | ✓ |
| 3D→4D mean | ~86.1% | 86.1% | ✓ |
| Overall mean | ~86.0% | 86.0% | ✓ |
| CV across sizes | ~2.8% | 2.8% | ✓ |

**Acceptance criteria:** Your results within ±2% of published values

### Step 3: Generate Figures

```bash
python generate_publication_figures.py
```

### Expected Output

```
======================================================================
PUBLICATION FIGURES GENERATOR
======================================================================

Loading multi-size validated data...
✓ Loaded multisize summary with 1,500 patterns
  - Grid sizes: 15, 17, 20, 23, 25
  - Mean losses: 1D→2D=85.8%, 2D→3D=86.1%, 3D→4D=86.1%
  - Overall: 86.0% ± 2.4%

Generating figures...
✓ Saved: Figure_1_Conceptual_Overview.png/pdf
✓ Saved: Figure_2_Loss_Distribution.png/pdf
✓ Saved: Figure_3_Rule_Independence.png/pdf
✓ Saved: Figure_4_Grid_Robustness.png/pdf
✓ Saved: Figure_5_Phi_Components.png/pdf
✓ Saved: Figure_6_Visual_Example.png/pdf
✓ Saved: Figure_7_Reverse_Prism.png/pdf

======================================================================
✓ ALL 7 FIGURES GENERATED
======================================================================
Location: publication_figures/
```

### Verify Figures

```bash
ls publication_figures/

# Should show:
# Figure_1_Conceptual_Overview.png
# Figure_1_Conceptual_Overview.pdf
# ... (14 files total: 7 PNG + 7 PDF)
```

**Visual verification:**
- Figure 1: Shows 1D→2D→3D cascade with ~86% losses
- Figure 2: Histogram centered around 86%
- Figure 4: Grid robustness showing consistency across sizes
- Figure 5: Bar chart showing Φ collapse across dimensions

## Pathway 3: Extended Validation

**Time:** ~3 hours  
**Goal:** Validate robustness across conditions

### Test 1: Grid Size Sensitivity (ALREADY DONE)

If you ran the full validation above, grid size sensitivity is already tested as part of the main validation. The multisize_summary_*.json file contains complete grid size analysis.

**Results already available:**
- All 5 grid sizes tested
- CV across sizes: ~2.8%
- Confirms scale-independence

### Test 2: Rule Independence

```bash
cd tests
python test_highlife_validation.py
```

**Expected:** HighLife loss ~86% (matches Conway's Life)

### Test 3: Metric Validation

```bash
python test_metric_sanity_check.py
```

**Expected:**
- All dead: Φ ≈ 0
- All alive: Φ ≈ 0
- Checkerboard: Φ > 0.5

## Troubleshooting

### Issue: Script takes too long

**Solution:** Test with fewer grid sizes first

```bash
# Edit validate_dimensional_cascade_multisize.py
# Change: GRID_SIZES = [15, 17, 20, 23, 25]
# To:     GRID_SIZES = [15, 20, 25]

# Run again (should take ~1.5 hours)
python validate_dimensional_cascade_multisize.py
```

### Issue: Different random results

**Cause:** Different numpy/python versions may produce different random sequences

**Solution:** Compare statistics, not exact values

```python
# Check if your results are statistically similar
your_mean = 85.5  # example
published_mean = 85.8
difference = abs(your_mean - published_mean)

if difference < 2.0:
    print("✓ Results match statistically")
```

### Issue: Import errors

**Solution:** Verify dependencies

```bash
pip install --upgrade numpy scipy matplotlib
python -c "import numpy; print(numpy.__version__)"  # Should be 1.21+
```

### Issue: Out of memory (4D tests, especially N=23 or N=25)

**Solution:** Reduce maximum grid size

```bash
# Edit validate_dimensional_cascade_multisize.py
# Change: GRID_SIZES = [15, 17, 20, 23, 25]
# To:     GRID_SIZES = [15, 17, 20]

# This avoids 23^4=279,841 and 25^4=390,625 cell arrays
```

## Verification Checklist

- [ ] Quick start example runs successfully
- [ ] Multi-size validation completes
- [ ] All 6 output files created in validation_results_multisize/
- [ ] Mean loss 1D→2D within 84-88%
- [ ] Mean loss 2D→3D within 84-88%
- [ ] Mean loss 3D→4D within 84-88%
- [ ] Overall mean within 84-88%
- [ ] CV across grid sizes 2-4%
- [ ] 7 figures generated successfully
- [ ] Figures show expected patterns (86% loss annotations, grid robustness)

## Statistical Replication

If you can't match exact values (different Python/numpy versions):

**Compare distributions:**

```python
import json
import numpy as np

# Load your results
with open('validation_results_multisize/multisize_summary_*.json') as f:
    your_data = json.load(f)

# Load published results
with open('validation_results_multisize/multisize_summary_20260113_*.json') as f:
    pub_data = json.load(f)

# Compare statistics
your_mean = your_data['consistency_analysis']['test_1d_2d']['mean_across_sizes']
pub_mean = pub_data['consistency_analysis']['test_1d_2d']['mean_across_sizes']

print(f"Your mean: {your_mean:.2f}%")
print(f"Published: {pub_mean:.2f}%")
print(f"Difference: {abs(your_mean - pub_mean):.2f}%")

# Acceptable if difference < 2%
```

## Citation for Replication

If you successfully replicate:

```bibtex
@misc{your_replication,
  title={Replication of: Universal Information Loss at Dimensional Boundaries},
  author={Your Name},
  year={2026},
  note={Successful replication of Thornhill (2026) using published code}
}
```

## Support

**Issues during replication:**
- Open GitHub issue with error details
- Include: OS, Python version, numpy version, error message
- Email: existencethreshold@gmail.com

**Response time:** 48-72 hours

## Success Criteria

✓ **Complete replication** if:
1. Mean loss within ±2% of published values per grid size
2. CV across grid sizes within ±1% of published value (2.8%)
3. Figures visually match published figures
4. All 7 figures generate without errors

✓ **Partial replication** if:
1. Mean loss within ±5% of published values
2. Distribution shape similar (histogram matches)
3. At least 5/7 figures generate correctly

⚠ **Failed replication** if:
1. Mean loss outside 80-92% range
2. High variance (CV >10%)
3. Systematic errors (memory issues, import errors)

**Report failures:** Open GitHub issue - helps improve reproducibility

---

**Last Updated:** January 2026  
**Estimated Success Rate:** >95% (based on beta testing)  
**Average Time:** 3 hours (including figure generation)
