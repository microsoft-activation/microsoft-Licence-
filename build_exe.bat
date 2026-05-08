@echo off 
cd /d "C:\Users\Adarsh Varma\Desktop\window" 
echo Building main_gui.exe... 
echo. 
pip install pyinstaller --quiet 
pyinstaller --onefile --windowed --icon=icon.ico --add-data "icon.ico;." main_gui.py 
echo. 
if exist "dist\main_gui.exe" ( 
    echo ✅ main_gui.exe created successfully! 
) else ( 
    echo ❌ Failed to create main_gui.exe 
) 
echo. 
pause 
