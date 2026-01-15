#!/bin/bash
# CLEANUP SCRIPT - Remove Generated Files
# Keeps: validated_results/, code, documentation
# Removes: publication_figures/, __pycache__, temp files
#
# Author: Nathan M. Thornhill
# Usage: ./cleanup.sh

echo ""
echo "========================================================================"
echo "REPOSITORY CLEANUP"
echo "========================================================================"
echo ""
echo "This will remove generated files and return repository to clean state:"
echo ""
echo "WILL DELETE:"
echo "  - publication_figures/ (can be regenerated)"
echo "  - __pycache__/ directories"
echo "  - *.pyc files"
echo "  - *.log files"
echo "  - Temporary files"
echo ""
echo "WILL KEEP:"
echo "  - validated_results/ (your data is safe!)"
echo "  - All code files"
echo "  - All documentation"
echo "  - examples/"
echo "  - tests/"
echo ""
read -p "Press Enter to continue or Ctrl+C to cancel..."

echo ""
echo "[1/5] Removing publication_figures/..."
if [ -d "publication_figures" ]; then
    rm -rf "publication_figures"
    echo "      [OK] Removed publication_figures/"
else
    echo "      [SKIP] Directory not found"
fi

echo ""
echo "[2/5] Removing __pycache__ directories..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
echo "      [OK] Removed __pycache__ directories"

echo ""
echo "[3/5] Removing .pyc files..."
find . -type f -name "*.pyc" -delete 2>/dev/null
echo "      [OK] Removed compiled Python files"

echo ""
echo "[4/5] Removing log files..."
find . -type f -name "*.log" -delete 2>/dev/null
echo "      [OK] Removed log files"

echo ""
echo "[5/5] Removing temporary files..."
find . -type f -name "*.tmp" -delete 2>/dev/null
echo "      [OK] Removed temporary files"

echo ""
echo "========================================================================"
echo "CLEANUP COMPLETE"
echo "========================================================================"
echo ""
echo "Your repository is now clean:"
echo "  ✓ Generated files removed"
echo "  ✓ Cache cleared"
echo "  ✓ Temporary files deleted"
echo ""
echo "Your data is safe:"
echo "  ✓ validated_results/ preserved"
echo "  ✓ All code intact"
echo "  ✓ Documentation unchanged"
echo ""
echo "To regenerate figures:"
echo "  python generate_publication_figures.py"
echo ""
