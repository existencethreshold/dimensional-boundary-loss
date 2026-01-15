#!/bin/bash
# UNINSTALL SCRIPT - Complete Removal (Preserves Data)
# Keeps ONLY: validated_results/
# Removes: Virtual environment, generated files, cache, figures
#
# Author: Nathan M. Thornhill
# Usage: ./uninstall.sh

echo ""
echo "========================================================================"
echo "REPOSITORY UNINSTALL"
echo "========================================================================"
echo ""
echo "⚠️  WARNING: This will remove nearly everything!"
echo ""
echo "WILL DELETE:"
echo "  - Virtual environments (venv/, env/, reviewer_env/)"
echo "  - publication_figures/"
echo "  - __pycache__/ directories"
echo "  - *.pyc files"
echo "  - *.log files"
echo "  - Temporary files"
echo ""
echo "WILL PRESERVE:"
echo "  - validated_results/ (YOUR DATA IS SAFE!)"
echo ""
echo "This is useful for:"
echo "  - Starting fresh after testing"
echo "  - Removing virtual environments"
echo "  - Cleaning before re-cloning"
echo ""
echo "⚠️  Are you SURE you want to proceed?"
echo ""
read -p "Press Enter to continue or Ctrl+C to cancel..."

echo ""
echo "[1/7] Removing virtual environments..."
for dir in venv env reviewer_env .venv; do
    if [ -d "$dir" ]; then
        rm -rf "$dir"
        echo "      [OK] Removed $dir/"
    fi
done

echo ""
echo "[2/7] Removing publication_figures/..."
if [ -d "publication_figures" ]; then
    rm -rf "publication_figures"
    echo "      [OK] Removed publication_figures/"
else
    echo "      [SKIP] Directory not found"
fi

echo ""
echo "[3/7] Removing __pycache__ directories..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
echo "      [OK] Removed __pycache__ directories"

echo ""
echo "[4/7] Removing .pyc files..."
find . -type f -name "*.pyc" -delete 2>/dev/null
echo "      [OK] Removed compiled Python files"

echo ""
echo "[5/7] Removing log files..."
find . -type f -name "*.log" -delete 2>/dev/null
echo "      [OK] Removed log files"

echo ""
echo "[6/7] Removing temporary files..."
find . -type f -name "*.tmp" -delete 2>/dev/null
echo "      [OK] Removed temporary files"

echo ""
echo "[7/7] Verifying validated_results/ is intact..."
if [ -d "validated_results" ]; then
    echo "      [OK] validated_results/ preserved ✓"
else
    echo "      [WARNING] validated_results/ directory not found"
fi

echo ""
echo "========================================================================"
echo "UNINSTALL COMPLETE"
echo "========================================================================"
echo ""
echo "Removed:"
echo "  ✓ Virtual environments"
echo "  ✓ Generated files"
echo "  ✓ Cache and temporary files"
echo ""
echo "Preserved:"
echo "  ✓ validated_results/ (YOUR DATA)"
echo "  ✓ Core code files"
echo "  ✓ Documentation"
echo ""
echo "What remains:"
echo "  - Code files (.py)"
echo "  - Documentation (.md)"
echo "  - Data files (.json in validated_results/)"
echo "  - Test scripts"
echo "  - Examples"
echo ""
echo "To set up again:"
echo "  1. python -m venv venv"
echo "  2. source venv/bin/activate"
echo "  3. pip install -r requirements.txt"
echo ""
