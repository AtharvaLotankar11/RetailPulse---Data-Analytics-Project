@echo off
echo ========================================
echo   RetailPulse Analytics Suite
echo   Starting Streamlit Application...
echo ========================================
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Run Streamlit
streamlit run dashboard\Home.py

pause
