@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ============================================
echo   CLI Selector Build Script
echo ============================================

if not exist "CLISelector.py" (
    echo [Error] CLISelector.py not found!
    pause
    exit
)

python -m PyInstaller --noconfirm --onefile --windowed --name="CLISelector" --collect-all "tkinterdnd2" --icon="resources\CLI.ico" --add-data "function;function" --add-data "gui;gui" --hidden-import="tkinterdnd2" --hidden-import="tkinterdnd2.TkinterDnD" --distpath="C:/Users/EJI1WX/OneDrive - Bosch Group/Program" --workpath="C:/Temp_Build" --clean CLISelector.py

echo.
echo --------------------------------------------
echo Build completed! EXE: CLISelector.exe
echo Output: C:/Users/EJI1WX/OneDrive - Bosch Group/Program
echo --------------------------------------------
pause