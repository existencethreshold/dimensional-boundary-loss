# Universal Information Loss at Dimensional Boundaries

**~86% information loss when embedding patterns across dimensional transitions in discrete computational systems**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Version](https://img.shields.io/badge/version-1.1.0-green.svg)](https://github.com/existencethreshold/dimensional-boundary-loss/releases)

## 📊 Key Finding

When embedding patterns from lower to higher dimensions, approximately **86% of measured information is lost** at each dimensional boundary—consistently across:

- **Dimensions tested:** 1D→2D (85.8%), 2D→3D (86.1%), 3D→4D (86.1%)
- **Pattern independence:** N=1,500 patterns across all transitions
- **Scale independence:** Robust across grid sizes N ∈ {15, 17, 20, 23, 25}
- **Rule independence:** Conway (86.5%) vs HighLife (87.1%) - 0.6% difference
- **Geometric origin:** Loss occurs from embedding itself, not pattern dynamics

## 🎯 Significance

This finding reveals a **universal geometric scaling law** in discrete systems with implications for:

- **Information Theory:** Quantifies dimensional embedding cost
- **Computational Complexity:** Pattern persistence across dimensions
- **Machine Learning:** Theoretical bound on dimensionality reduction
- **Consciousness Studies:** Potential mechanism for dimensional dispersion hypothesis

## 🚀 Quick Start

### Installation

```bash
git clone https://github.com/existencethreshold/dimensional-boundary-loss
cd dimensional-boundary-loss
pip install -r requirements.txt
```

**Requirements:** Python 3.8+, numpy, scipy, matplotlib

### Run Full Validation (~2.5 hours)

```bash
python validate_dimensional_cascade_multisize.py
```

This tests grid size robustness across N ∈ {15, 17, 20, 23, 25}:
- 100 patterns per grid size, all 3 transitions
- Total: 1,500 patterns
- Results: Mean loss **86.0% ± 2.4%** (CV = 2.8%)

Output files:
```
validation_results_multisize/dimensional_cascade_N100_grid15_*.json
validation_results_multisize/dimensional_cascade_N100_grid17_*.json
validation_results_multisize/dimensional_cascade_N100_grid20_*.json
validation_results_multisize/dimensional_cascade_N100_grid23_*.json
validation_results_multisize/dimensional_cascade_N100_grid25_*.json
validation_results_multisize/multisize_summary_*.json
```

### Generate Publication Figures

```bash
python generate_publication_figures.py
```

Creates 7 figures in `publication_figures/` (PNG and PDF formats).

### Quick Example (1D→2D)

```bash
python examples/quick_start.py
```

Expected output: **~86% loss**

## 📖 Documentation

- **[CHANGELOG.md](CHANGELOG.md)** - Version history
- **[METHODOLOGY.md](docs/METHODOLOGY.md)** - Detailed methods and statistical approach
- **[PHI_METRIC.md](docs/PHI_METRIC.md)** - The Φ metric: R·S + D explained
- **[REPLICATION.md](docs/REPLICATION.md)** - Step-by-step replication guide

## 📁 Repository Structure

```
dimensional-boundary-loss/
├── README.md
├── CHANGELOG.md                 # Version history
├── LICENSE
├── requirements.txt
├── .gitignore
│
├── validate_dimensional_cascade_multisize.py
├── generate_publication_figures.py
│
├── cleanup.bat                  # Windows cleanup
├── cleanup.sh                   # Linux/Mac cleanup
├── uninstall.bat                # Windows uninstall
├── uninstall.sh                 # Linux/Mac uninstall
├── cleanup_utility.py           # Cross-platform utility
│
├── validation_results_multisize/
│   ├── dimensional_cascade_N100_grid15_*.json
│   ├── dimensional_cascade_N100_grid17_*.json
│   ├── dimensional_cascade_N100_grid20_*.json
│   ├── dimensional_cascade_N100_grid23_*.json
│   ├── dimensional_cascade_N100_grid25_*.json
│   └── multisize_summary_*.json
│
├── publication_figures/
│   ├── Figure_1_*.png/pdf
│   ├── Figure_2_*.png/pdf
│   ├── Figure_3_*.png/pdf
│   ├── Figure_4_*.png/pdf
│   ├── Figure_5_*.png/pdf
│   ├── Figure_6_*.png/pdf
│   └── Figure_7_*.png/pdf
│
├── examples/
│   └── quick_start.py
│
├── tests/
│   ├── test_grid_size_sensitivity.py
│   ├── test_highlife_validation.py
│   ├── test_metric_sanity_check.py
│   └── validation_data/
│       ├── grid_size_validation_*.json
│       ├── highlife_validation_*.json
│       └── metric_sanity_check_*.json
│
└── docs/
    ├── METHODOLOGY.md
    ├── PHI_METRIC.md
    ├── REPLICATION.md
    └── CLEANUP.md              
```

## 🔬 The Φ (Phi) Metric

Measures pattern persistence/information:

```
Φ = R·S + D

Where:
  R = Processing (alive cells / total cells)
  S = Integration (spatial transitions / total edges)
  D = Disorder (Shannon entropy of state distribution)
```

**Higher Φ = more active information processing**

See [PHI_METRIC.md](docs/PHI_METRIC.md) for detailed explanation.

## 📈 Results Summary

### Overall Finding (Across All Grid Sizes)

| Metric | Value |
|--------|-------|
| Mean Loss | **86.0% ± 2.4%** |
| Range | 82.5% - 88.6% |
| Grid Sizes Tested | 15, 17, 20, 23, 25 |
| Total Patterns | 1,500 |
| Coefficient of Variation | 2.8% |

### By Transition (Mean Across Grid Sizes)

| Transition | Mean Loss | Range | CV |
|-----------|-----------|-------|-----|
| 1D→2D | 85.8% | 82.5%-88.5% | 2.9% |
| 2D→3D | 86.1% | 83.0%-88.6% | 2.7% |
| 3D→4D | 86.1% | 83.0%-88.6% | 2.7% |

**Interpretation:** Universal ~86% loss across all grid sizes and dimensional transitions, with expected finite-size variation

### Rule Independence

| Rule | Mean Loss | Configuration |
|------|-----------|---------------|
| Conway | **86.5%** | B3/S23 (Birth/Survival) |
| HighLife | **87.1%** | B36/S23 |
| Difference | **0.6%** | Effect is geometric, not rule-dependent |

## 🔁 Replication

### Full Validation (Recommended)

```bash
python validate_dimensional_cascade_multisize.py
```

- **Runtime:** ~2.5 hours (tests 5 grid sizes)
- **Output:** `validation_results_multisize/` directory with 6 JSON files
- **Verification:** Compare statistics with published results
  - Mean loss: ~86.0%
  - CV across sizes: ~2.8%

### Grid Size Robustness Details

The validation tests demonstrate:
- **Scale-independence:** ~86% loss holds from 15×15 to 25×25 grids
- **Realistic variation:** CV = 2.8% shows expected finite-size effects
- **Consistency:** All three transitions cluster around 86%

### Quick Verification

```bash
# Test single transition
python examples/quick_start.py

# Expected: 80-92% loss (pattern-dependent)
# Mean across many patterns: ~86%
```

### Validate Robustness

```bash
cd tests

# Grid size sensitivity (15-25)
python test_grid_size_sensitivity.py

# Rule independence (Conway vs HighLife)
python test_highlife_validation.py

# Metric validation (edge cases)
python test_metric_sanity_check.py
```

See [REPLICATION.md](docs/REPLICATION.md) for detailed instructions.

## 📊 Figures

Run `python generate_publication_figures.py` to generate:

1. **Figure 1:** Conceptual overview (1D→2D→3D cascade)
2. **Figure 2:** Loss distribution histogram (N=1,500)
3. **Figure 3:** Rule independence - Conway (86.5%) vs HighLife (87.1%)
4. **Figure 4:** Grid size robustness (N ∈ {15, 17, 20, 23, 25})
5. **Figure 5:** Φ metric components (R, S decomposition)
6. **Figure 6:** Visual embedding example (1D→2D)
7. **Figure 7:** Reverse Prism hypothesis

## 🧹 Repository Maintenance

### Cleanup Generated Files

After running validation or generating figures, you can clean up:

```bash
# Remove generated files (keeps validation_results_multisize/)
cleanup.bat     # Windows
./cleanup.sh    # Linux/Mac
python cleanup_utility.py cleanup  # Cross-platform
```

**Removes:** publication_figures/, __pycache__, temp files  
**Keeps:** validation_results_multisize/, code, documentation

### Uninstall (Remove Virtual Environment)

Remove everything except validation_results_multisize/:

```bash
# Remove venv and generated files (keeps data)
uninstall.bat   # Windows
./uninstall.sh  # Linux/Mac
python cleanup_utility.py uninstall  # Cross-platform
```

**Removes:** Virtual environments, generated files, cache  
**Keeps:** validation_results_multisize/, code, documentation

### Reset to Fresh State (DELETES DATA!)

⚠️ **Warning:** This deletes validation_results_multisize/

```bash
# Complete reset (use with caution!)
python cleanup_utility.py reset
```

**Use when:** Starting completely fresh, re-running full validation

See [CLEANUP.md](docs/CLEANUP.md) for detailed documentation.

---

## 📝 Citation

```bibtex
@article{thornhill2026dimensional,
  title={Pattern Loss at Dimensional Boundaries: The 86% Scaling Law},
  author={Thornhill, Nathan M.},
  journal={PLOS Complex Systems},
  year={2026},
  note={In review},
  doi={10.5281/zenodo.18238486}
}
```

## 🤝 Contributing

This repository contains published research code. To contribute:

1. **Report issues:** Open GitHub issue for bugs/questions
2. **Suggest improvements:** Submit pull request with clear description
3. **Extend research:** Fork and cite if building on this work

## 📄 License

MIT License - see [LICENSE](LICENSE) file

**Summary:** Free to use, modify, and distribute with attribution

## 👤 Author

**Nathan M. Thornhill**  
Independent Researcher  
Fort Wayne, Indiana, USA

- **Email:** existencethreshold@gmail.com
- **ORCID:** 0009-0009-3161-528X
- **GitHub:** https://github.com/existencethreshold

## Recent Publications

**Pattern Loss at Dimensional Boundaries: The 86% Scaling Law** (2026)
- Zenodo: https://doi.org/10.5281/zenodo.18238485
- Code: https://github.com/existencethreshold/dimensional-boundary-loss
- Status: Peer review (PLOS Complex Systems)

**The Existence Threshold v2.1** (2026)
- DOI: https://doi.org/10.5281/zenodo.18124074

## 🙏 Acknowledgments

- Anthropic Claude (computational research assistance)
- Open source cellular automata community
- Peer reviewers and community feedback

---

**Last Updated:** January 15, 2026  
**Status:** Peer review (PLOS Complex Systems)  
**DOI:** 10.5281/zenodo.18238486  
**Version:** 1.1.0
