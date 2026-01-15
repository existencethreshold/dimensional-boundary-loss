@echo off
REM CLEANUP SCRIPT - Remove Generated Files
REM Keeps: validated_results/, code, documentation
REM Removes: publication_figures/, __pycache__, temp files
REM
REM Author: Nathan M. Thornhill
REM Usage: cleanup.bat

echo.
echo ========================================================================
echo REPOSITORY CLEANUP
echo ========================================================================
echo.
echo This will remove generated files and return repository to clean state:
echo.
echo WILL DELETE:
echo   - publication_figures/ (can be regenerated)
echo   - __pycache__/ directories
echo   - *.pyc files
echo   - *.log files
echo   - Temporary files
echo.
echo WILL KEEP:
echo   - validated_results/ (your data is safe!)
echo   - All code files
echo   - All documentation
echo   - examples/
echo   - tests/
echo.
echo Press Ctrl+C to cancel, or
pause

echo.
echo [1/5] Removing publication_figures/...
if exist "publication_figures" (
    rmdir /s /q "publication_figures"
    echo       [OK] Removed publication_figures/
) else (
    echo       [SKIP] Directory not found
)

echo.
echo [2/5] Removing __pycache__ directories...
for /d /r %%d in (__pycache__) do (
    if exist "%%d" (
        rmdir /s /q "%%d"
        echo       [OK] Removed %%d
    )
)

echo.
echo [3/5] Removing .pyc files...
del /s /q *.pyc >nul 2>&1
if %errorlevel%==0 (
    echo       [OK] Removed compiled Python files
) else (
    echo       [SKIP] No .pyc files found
)

echo.
echo [4/5] Removing log files...
del /s /q *.log >nul 2>&1
if %errorlevel%==0 (
    echo       [OK] Removed log files
) else (
    echo       [SKIP] No log files found
)

echo.
echo [5/5] Removing temporary files...
del /s /q *.tmp >nul 2>&1
if %errorlevel%==0 (
    echo       [OK] Removed temporary files
) else (
    echo       [SKIP] No temp files found
)

echo.
echo ========================================================================
echo CLEANUP COMPLETE
echo ========================================================================
echo.
echo Your repository is now clean:
echo   ✓ Generated files removed
echo   ✓ Cache cleared
echo   ✓ Temporary files deleted
echo.
echo Your data is safe:
echo   ✓ validated_results/ preserved
echo   ✓ All code intact
echo   ✓ Documentation unchanged
echo.
echo To regenerate figures:
echo   python generate_publication_figures.py
echo.
pause
