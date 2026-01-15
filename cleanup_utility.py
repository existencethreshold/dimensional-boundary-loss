"""
Repository Cleanup Utility
Cross-platform script for cleaning generated files

Options:
  cleanup  - Remove generated files (keeps validated_results/)
  uninstall - Remove everything except validated_results/
  reset    - Full reset to fresh download state

Author: Nathan M. Thornhill
Usage: python cleanup_utility.py [cleanup|uninstall|reset]
"""

import os
import shutil
import sys
from pathlib import Path


def get_size_mb(path):
    """Calculate directory size in MB"""
    total = 0
    try:
        for entry in os.scandir(path):
            if entry.is_file():
                total += entry.stat().st_size
            elif entry.is_dir():
                total += get_size_mb(entry.path)
    except PermissionError:
        pass
    return total / (1024 * 1024)


def cleanup_generated_files():
    """Remove generated files, keep validated_results/"""
    
    print("="*70)
    print("CLEANUP: Remove Generated Files")
    print("="*70)
    print()
    print("Will remove:")
    print("  - publication_figures/")
    print("  - __pycache__/ directories")
    print("  - *.pyc files")
    print("  - *.log files")
    print()
    print("Will keep:")
    print("  - validated_results/")
    print("  - All code and documentation")
    print()
    
    confirm = input("Continue? [y/N]: ")
    if confirm.lower() != 'y':
        print("Cancelled.")
        return
    
    removed_count = 0
    saved_bytes = 0
    
    # Remove publication_figures/
    if os.path.exists("publication_figures"):
        size = get_size_mb("publication_figures")
        shutil.rmtree("publication_figures")
        print(f"✓ Removed publication_figures/ ({size:.1f} MB)")
        removed_count += 1
        saved_bytes += size
    
    # Remove __pycache__
    for root, dirs, files in os.walk("."):
        if "__pycache__" in dirs:
            pycache = os.path.join(root, "__pycache__")
            size = get_size_mb(pycache)
            shutil.rmtree(pycache)
            saved_bytes += size
            removed_count += 1
    print(f"✓ Removed __pycache__ directories")
    
    # Remove .pyc files
    pyc_count = 0
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".pyc"):
                os.remove(os.path.join(root, file))
                pyc_count += 1
    if pyc_count > 0:
        print(f"✓ Removed {pyc_count} .pyc files")
    
    # Remove log files
    log_count = 0
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".log"):
                os.remove(os.path.join(root, file))
                log_count += 1
    if log_count > 0:
        print(f"✓ Removed {log_count} log files")
    
    print()
    print("="*70)
    print("CLEANUP COMPLETE")
    print("="*70)
    print(f"Freed {saved_bytes:.1f} MB")
    print()
    print("✓ validated_results/ preserved")
    print("✓ All code intact")
    print()


def uninstall_all():
    """Remove everything except validated_results/"""
    
    print("="*70)
    print("UNINSTALL: Complete Removal")
    print("="*70)
    print()
    print("⚠️  WARNING: This removes nearly everything!")
    print()
    print("Will remove:")
    print("  - Virtual environments")
    print("  - publication_figures/")
    print("  - __pycache__/")
    print("  - All generated/temporary files")
    print()
    print("Will PRESERVE:")
    print("  - validated_results/ (YOUR DATA)")
    print("  - Core code files")
    print("  - Documentation")
    print()
    
    confirm = input("Are you SURE? Type 'yes' to confirm: ")
    if confirm.lower() != 'yes':
        print("Cancelled.")
        return
    
    removed_count = 0
    saved_bytes = 0
    
    # Remove virtual environments
    venv_names = ['venv', 'env', 'reviewer_env', '.venv']
    for venv in venv_names:
        if os.path.exists(venv):
            size = get_size_mb(venv)
            shutil.rmtree(venv)
            print(f"✓ Removed {venv}/ ({size:.1f} MB)")
            saved_bytes += size
            removed_count += 1
    
    # Remove publication_figures/
    if os.path.exists("publication_figures"):
        size = get_size_mb("publication_figures")
        shutil.rmtree("publication_figures")
        print(f"✓ Removed publication_figures/ ({size:.1f} MB)")
        saved_bytes += size
    
    # Remove __pycache__
    for root, dirs, files in os.walk("."):
        if "__pycache__" in dirs:
            pycache = os.path.join(root, "__pycache__")
            shutil.rmtree(pycache)
    print(f"✓ Removed __pycache__ directories")
    
    # Remove .pyc, .log, .tmp files
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith((".pyc", ".log", ".tmp")):
                os.remove(os.path.join(root, file))
    print(f"✓ Removed temporary files")
    
    # Verify validated_results/ exists
    if os.path.exists("validated_results"):
        print()
        print("✓ validated_results/ PRESERVED")
    
    print()
    print("="*70)
    print("UNINSTALL COMPLETE")
    print("="*70)
    print(f"Freed {saved_bytes:.1f} MB")
    print()
    print("To set up again:")
    print("  1. python -m venv venv")
    print("  2. source venv/bin/activate  (Windows: venv\\Scripts\\activate)")
    print("  3. pip install -r requirements.txt")
    print()


def reset_to_fresh():
    """Reset to fresh download state (removes ALL generated data including validated_results)"""
    
    print("="*70)
    print("RESET: Return to Fresh Download State")
    print("="*70)
    print()
    print("⚠️⚠️⚠️  DANGER: This removes EVERYTHING generated!")
    print()
    print("Will remove:")
    print("  - validated_results/ (YOUR DATA WILL BE DELETED!)")
    print("  - Virtual environments")
    print("  - publication_figures/")
    print("  - All generated/temporary files")
    print()
    print("Will keep ONLY:")
    print("  - Core code files")
    print("  - Documentation")
    print("  - Examples")
    print("  - Test scripts")
    print()
    print("This returns the repository to exactly as downloaded.")
    print("You will need to re-run validation to generate data.")
    print()
    
    confirm = input("Are you ABSOLUTELY SURE? Type 'DELETE MY DATA' to confirm: ")
    if confirm != 'DELETE MY DATA':
        print("Cancelled.")
        return
    
    # Remove validated_results/
    if os.path.exists("validated_results"):
        shutil.rmtree("validated_results")
        os.makedirs("validated_results")  # Recreate empty
        print("✓ Removed validated_results/")
    
    # Remove tests/ results
    if os.path.exists("tests"):
        for file in os.listdir("tests"):
            if file.endswith(".json"):
                os.remove(os.path.join("tests", file))
        print("✓ Removed test results")
    
    # Run uninstall
    uninstall_all()
    
    print()
    print("="*70)
    print("RESET COMPLETE")
    print("="*70)
    print()
    print("Repository is now in fresh download state.")
    print()
    print("To generate data:")
    print("  python validate_dimensional_cascade_unified.py")
    print()


def show_usage():
    """Show usage information"""
    print()
    print("Repository Cleanup Utility")
    print("="*70)
    print()
    print("Usage: python cleanup_utility.py [option]")
    print()
    print("Options:")
    print("  cleanup    - Remove generated files (keeps validated_results/)")
    print("  uninstall  - Remove everything except validated_results/")
    print("  reset      - Full reset to fresh state (DELETES ALL DATA)")
    print()
    print("Examples:")
    print("  python cleanup_utility.py cleanup     # Clean up after testing")
    print("  python cleanup_utility.py uninstall   # Remove virtual env")
    print("  python cleanup_utility.py reset       # Start completely fresh")
    print()


def main():
    """Main function"""
    
    if len(sys.argv) < 2:
        show_usage()
        return
    
    option = sys.argv[1].lower()
    
    if option == "cleanup":
        cleanup_generated_files()
    elif option == "uninstall":
        uninstall_all()
    elif option == "reset":
        reset_to_fresh()
    else:
        print(f"Unknown option: {option}")
        show_usage()


if __name__ == "__main__":
    main()
