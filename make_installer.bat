@echo off
cd /d "C:\Users\Adarsh Varma\Desktop\window"
echo ========================================
echo    Creating Installer
echo ========================================
echo.
echo Checking required files...
echo.

if not exist "icon.ico" (
    echo ❌ ERROR: icon.ico not found!
    echo Please create an icon.ico file first
    pause
    exit /b 1
)

if not exist "dist\main_gui.exe" (
    echo ❌ ERROR: main_gui.exe not found!
    echo Please run build_exe.bat first
    pause
    exit /b 1
)

echo ✓ All files found
echo.
echo Step 1: Checking Inno Setup...
echo.

set "INNO_PATH1=C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
set "INNO_PATH2=C:\Program Files\Inno Setup 6\ISCC.exe"

if exist "%INNO_PATH1%" (
    set "INNO_PATH=%INNO_PATH1%"
) else if exist "%INNO_PATH2%" (
    set "INNO_PATH=%INNO_PATH2%"
) else (
    echo ❌ Inno Setup not found!
    echo Please install Inno Setup or compile manually
    echo.
    echo Manual steps:
    echo 1. Open Inno Setup Compiler
    echo 2. File -> Open -> select setup_script.iss
    echo 3. Click Compile button (green arrow)
    pause
    exit /b 1
)

echo ✓ Inno Setup found at: %INNO_PATH%
echo.
echo Step 2: Compiling installer...
echo.

"%INNO_PATH%" setup_script.iss

echo.
if exist "Output\WindowsActivatorSetup.exe" (
    echo ✅ SUCCESS! Installer created!
    echo.
    echo 📁 Installer location: %cd%\Output\WindowsActivatorSetup.exe
    echo 📦 Size: 
    for %%F in ("Output\WindowsActivatorSetup.exe") do echo %%~zF bytes
    echo.
    echo 🚀 You can now distribute this installer!
) else (
    echo ❌ Installer not created. Check errors above.
)

echo.
pause