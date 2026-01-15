# ERRATA

## Paper: "Pattern Loss at Dimensional Boundaries: The 86% Scaling Law"
**Author:** Nathan M. Thornhill  
**Date of Original Publication:** January 13, 2026  
**Correction Date:** January 15, 2026

---

## ERRATUM: Figure 3 Data Inaccuracy (v1.0 → v1.1)

### Summary
Figure 3 in version 1.0 of the paper displayed placeholder values instead of actual experimental validation data. This erratum corrects the figure to show the true experimental results.

### Location
**Figure 3:** "Rule Independence: Conway vs HighLife (Geometric effect independent of dynamics)"

### Error Description
The figure generation script (`generate_publication_figures.py`) contained a function that was never updated from its placeholder implementation to load actual validation data. As a result, Figure 3 displayed:

**Published (Incorrect):**
- Conway's Game of Life (B3/S23): 86.0%
- HighLife (B36/S23): 86.2%
- Difference: 0.2%

**Should Have Displayed (Correct):**
- Conway's Game of Life (B3/S23): 86.5% (actual: 86.46%)
- HighLife (B36/S23): 87.1% (actual: 87.11%)
- Difference: 0.6% (actual: 0.64%)

### Text Accuracy
The paper's text (Page 15) correctly states the actual values:
> "The mean loss differed by only 0.64% (86.46% vs 87.11%)."

The text was accurate; only the figure was incorrect.

### Root Cause
During development of the figure generation pipeline, a placeholder function was created with temporary hardcoded values (86.0%, 86.2%) to test the visualization layout. The function was marked with a comment:
```python
"""Figure 3: Rule independence (placeholder - requires HighLife data)"""
```

The function was never updated to load the actual data from:
- `validation_results_multisize/multisize_summary_20260115_144513.json` (Conway data)
- `tests/validation_data/highlife_validation_20260113_035936.json` (HighLife data)

### Impact Assessment

**NO IMPACT ON:**
- ✅ Raw validation data (always correct)
- ✅ Experimental methodology (unchanged)
- ✅ Statistical analysis (unchanged)
- ✅ Paper conclusions (unchanged)
- ✅ Text descriptions (always correct)
- ✅ Table 1 values (always correct)
- ✅ Other figures (Figures 1, 2, 4, 5, 6, 7 - all correct)

**IMPACT:**
- ❌ Figure 3 visual representation did not match text
- ❌ Minor discrepancy between stated and displayed values (~0.4%)
- ❌ Could cause confusion about rule independence findings

### Correction
**Version 1.1** corrects this error by:
1. Updating `generate_publication_figures.py` to load actual validation data
2. Regenerating all figures with correct data
3. Verifying all figures against source validation files

### Verification
The corrected values have been verified against the original validation data files:

```
Conway (B3/S23) - Source Data:
  File: validation_results_multisize/multisize_summary_20260115_144513.json
  Path: results_by_size.grid_20.test_2d_3d.mean_loss_pct
  Raw Value: 86.46389659945197%
  Displayed: 86.5%

HighLife (B36/S23) - Source Data:
  File: tests/validation_data/highlife_validation_20260113_035936.json
  Path: statistics.mean_loss  
  Raw Value: 87.10646329830824%
  Displayed: 87.1%

Difference: 0.64257669885627% (displayed as 0.6%)
```

### How to Obtain Corrected Version
- **GitHub:** https://github.com/existencethreshold/dimensional-boundary-loss (v1.1.0)
- **Zenodo:** [Updated DOI] (v1.1)
- **Pre-print:** [Updated link if applicable]

### Acknowledgment
This error was discovered during post-publication validation on January 15, 2026. We thank the validation process for identifying this discrepancy and apologize for any confusion caused by the incorrect figure.

### Contact
For questions regarding this erratum, please contact:
- Nathan M. Thornhill
- Email: [your email if you want to include it]
- GitHub: https://github.com/existencethreshold/dimensional-boundary-loss/issues

---

**Statement of Scientific Integrity:**

The underlying experimental data, methodology, and conclusions of this work remain valid and unchanged. This correction addresses only a figure generation error that caused a mismatch between the text and visual representation. All raw data, validation scripts, and analysis code have been publicly available since initial publication and can be independently verified.
