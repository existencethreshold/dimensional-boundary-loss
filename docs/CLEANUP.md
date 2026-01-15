# Repository Cleanup Utilities

Tools for managing generated files and maintaining a clean repository.

## 📋 Available Tools

### 1. cleanup - Clean Generated Files

**Removes:**
- `publication_figures/` (can be regenerated)
- `__pycache__/` directories
- `*.pyc` compiled Python files
- `*.log` log files
- `*.tmp` temporary files

**Keeps:**
- ✅ `validation_results_multisize/` (YOUR DATA)
- ✅ All code files
- ✅ All documentation
- ✅ Virtual environment (if exists)

**Use when:**
- After generating figures (clean up before committing)
- Testing complete, want clean state
- Preparing to regenerate outputs

**How to use:**

```bash
# Windows
cleanup.bat

# Linux/Mac
./cleanup.sh

# Cross-platform (Python)
python cleanup_utility.py cleanup
```

---

### 2. uninstall - Remove Everything (Except Data)

**Removes:**
- Virtual environments (`venv/`, `env/`, `reviewer_env/`)
- `publication_figures/`
- `__pycache__/` directories
- All compiled and temporary files

**Keeps:**
- ✅ `validation_results_multisize/` (YOUR DATA PRESERVED)
- ✅ Core code files
- ✅ Documentation

**Use when:**
- Done with testing, want to clean up
- Removing virtual environment
- Preparing to archive/transfer repository
- Want fresh Python environment

**How to use:**

```bash
# Windows
uninstall.bat

# Linux/Mac
./uninstall.sh

# Cross-platform (Python)
python cleanup_utility.py uninstall
```

**After uninstall, to set up again:**
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

### 3. reset - Complete Reset (DELETES DATA!)

**⚠️ WARNING: This DELETES validation_results_multisize/**

**Removes:**
- ❌ `validation_results_multisize/` (ALL YOUR DATA)
- Virtual environments
- `publication_figures/`
- Test results
- Everything generated

**Keeps ONLY:**
- Core code files
- Documentation
- Examples
- Test scripts

**Use when:**
- Want to start completely fresh
- Re-running full validation from scratch
- Cleaning for redistribution
- **NEVER use if you want to keep your data!**

**How to use:**

```bash
# Cross-platform (Python only - too dangerous for shell scripts)
python cleanup_utility.py reset
```

---

## 🎯 Quick Reference

| Task | Command | Keeps Data? | Keeps VEnv? |
|------|---------|-------------|-------------|
| Clean outputs | `cleanup.bat/.sh` | ✅ Yes | ✅ Yes |
| Remove venv | `uninstall.bat/.sh` | ✅ Yes | ❌ No |
| Start fresh | `python cleanup_utility.py reset` | ❌ NO! | ❌ No |

---

## 💡 Common Scenarios

### Scenario 1: Generated Figures, Want Clean Repo

```bash
# Remove generated figures and cache
cleanup.bat  # or cleanup.sh on Linux/Mac

# Result: Clean repo, data preserved
```

### Scenario 2: Testing Complete, Remove Everything

```bash
# Remove virtual environment and generated files
uninstall.bat  # or uninstall.sh on Linux/Mac

# Result: Only code/docs/data remain
```

### Scenario 3: Want to Re-run Full Validation

```bash
# DANGER: This deletes your data!
python cleanup_utility.py reset

# Then re-run:
python validate_dimensional_cascade_multisize.py
```

### Scenario 4: Peer Reviewer Starting Fresh

```bash
# Clone repository
git clone https://github.com/existencethreshold/dimensional-boundary-loss
cd dimensional-boundary-loss

# Install
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Test
python examples/quick_start.py

# When done testing
./cleanup.sh  # Clean up generated files

# Or if removing everything
./uninstall.sh  # Removes venv too
```

---

## 🔒 Safety Features

### Confirmation Required
All scripts require confirmation before deleting files.

### Data Preservation
`cleanup` and `uninstall` ALWAYS preserve `validation_results_multisize/`

### Reset Safety
`reset` requires typing "DELETE MY DATA" to prevent accidents.

### Dry Run (Python utility)
```bash
# Preview what will be deleted (future feature)
python cleanup_utility.py cleanup --dry-run
```

---

## 📊 What Gets Removed

### cleanup removes:
```
publication_figures/
  ├── Figure_1_Conceptual_Overview.png
  ├── Figure_1_Conceptual_Overview.pdf
  └── ... (all 14 files)

__pycache__/
  └── *.pyc files

*.log files
*.tmp files
```

### uninstall removes (additional):
```
venv/  (or env/, reviewer_env/)
  └── (entire virtual environment)

Everything from cleanup
```

### reset removes (additional):
```
validation_results_multisize/
  └── *.json files  ⚠️ YOUR DATA

tests/
  └── *.json files  (test results)

Everything from uninstall
```

---

## ⚠️ Important Notes

### Data Safety
- `cleanup` and `uninstall` NEVER touch `validation_results_multisize/`
- Your data is safe unless you explicitly use `reset`
- Always backup important data before using `reset`

### Virtual Environments
- `cleanup` preserves virtual environments
- `uninstall` removes virtual environments
- Easy to recreate with `python -m venv venv`

### Cross-Platform
- `.bat` scripts for Windows
- `.sh` scripts for Linux/Mac
- `cleanup_utility.py` works everywhere

### Git Tracking
These generated files should already be in `.gitignore`:
```
publication_figures/
__pycache__/
*.pyc
*.log
venv/
env/
```

---

## 🚀 Best Practices

### For Developers
```bash
# After testing new features
cleanup.bat

# Commit clean code
git add .
git commit -m "Added feature X"
```

### For Peer Reviewers
```bash
# After completing review
uninstall.sh

# Keeps data for verification, removes environment
```

### For Clean Distribution
```bash
# Before creating release
python cleanup_utility.py cleanup

# Ensure only essential files remain
git status
```
---

**Questions?** See main [README.md](README.md) or open an issue.
