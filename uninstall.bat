@echo off
REM UNINSTALL SCRIPT - Complete Removal (Preserves Data)
REM Keeps ONLY: validated_results/
REM Removes: Virtual environment, generated files, cache, figures
REM
REM Author: Nathan M. Thornhill
REM Usage: uninstall.bat

echo.
echo ========================================================================
echo REPOSITORY UNINSTALL
echo ========================================================================
echo.
echo ⚠️  WARNING: This will remove nearly everything!
echo.
echo WILL DELETE:
echo   - Virtual environments (venv/, env/, reviewer_env/)
echo   - publication_figures/
echo   - __pycache__/ directories
echo   - *.pyc files
echo   - *.log files
echo   - Temporary files
echo.
echo WILL PRESERVE:
echo   - validated_results/ (YOUR DATA IS SAFE!)
echo.
echo This is useful for:
echo   - Starting fresh after testing
echo   - Removing virtual environments
echo   - Cleaning before re-cloning
echo.
echo ⚠️  Are you SURE you want to proceed?
echo.
pause

echo.
echo [1/7] Removing virtual environments...
for %%d in (venv env reviewer_env .venv) do (
    if exist "%%d" (
        rmdir /s /q "%%d"
        echo       [OK] Removed %%d/
    )
)

echo.
echo [2/7] Removing publication_figures/...
if exist "publication_figures" (
    rmdir /s /q "publication_figures"
    echo       [OK] Removed publication_figures/
) else (
    echo       [SKIP] Directory not found
)

echo.
echo [3/7] Removing __pycache__ directories...
for /d /r %%d in (__pycache__) do (
    if exist "%%d" (
        rmdir /s /q "%%d"
        echo       [OK] Removed %%d
    )
)

echo.
echo [4/7] Removing .pyc files...
del /s /q *.pyc >nul 2>&1
echo       [OK] Removed compiled Python files

echo.
echo [5/7] Removing log files...
del /s /q *.log >nul 2>&1
echo       [OK] Removed log files

echo.
echo [6/7] Removing temporary files...
del /s /q *.tmp >nul 2>&1
echo       [OK] Removed temporary files

echo.
echo [7/7] Verifying validated_results/ is intact...
if exist "validated_results" (
    echo       [OK] validated_results/ preserved ✓
) else (
    echo       [WARNING] validated_results/ directory not found
)

echo.
echo ========================================================================
echo UNINSTALL COMPLETE
echo ========================================================================
echo.
echo Removed:
echo   ✓ Virtual environments
echo   ✓ Generated files
echo   ✓ Cache and temporary files
echo.
echo Preserved:
echo   ✓ validated_results/ (YOUR DATA)
echo   ✓ Core code files
echo   ✓ Documentation
echo.
echo What remains:
echo   - Code files (.py)
echo   - Documentation (.md)
echo   - Data files (.json in validated_results/)
echo   - Test scripts
echo   - Examples
echo.
echo To set up again:
echo   1. python -m venv venv
echo   2. venv\Scripts\activate
echo   3. pip install -r requirements.txt
echo.
pause
