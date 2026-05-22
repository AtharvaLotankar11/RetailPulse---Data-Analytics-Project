@echo off
echo ========================================
echo RetailPulse Dashboard - Quick Start
echo ========================================
echo.
echo Stopping any running Streamlit instances...
taskkill /F /IM streamlit.exe 2>nul
timeout /t 2 >nul
echo.
echo Starting RetailPulse Dashboard...
echo.
cd /d "%~dp0"
call venv\Scripts\activate
venv\Scripts\streamlit.exe run dashboard\Home.py
