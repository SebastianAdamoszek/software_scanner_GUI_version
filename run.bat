@echo off
echo Starting Software Inventory Scanner...
python app.py

if errorlevel 1 (
    echo.
    echo Program finished with an error.
    pause
    exit /b 1
)

echo.
echo Program finished successfully.
pause
