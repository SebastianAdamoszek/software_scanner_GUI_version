@echo off
echo Installing project dependencies...
python -m pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo Dependency installation failed.
    echo Check if Python is installed and available in PATH.
    pause
    exit /b 1
)

echo.
echo Dependencies installed successfully.
pause
