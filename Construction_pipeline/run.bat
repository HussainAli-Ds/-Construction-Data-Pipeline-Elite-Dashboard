@echo off
title 🚀 Construction Pipeline System

echo ==========================================
echo 🚀 Starting Full System...
echo ==========================================

cd /d %~dp0

REM -------------------------------
REM Start Pipeline
REM -------------------------------
echo 🔄 Starting Pipeline...
start "Pipeline" cmd /k "cd code && python main.py"

REM -------------------------------
REM Start Dashboard
REM -------------------------------
echo 📊 Starting Dashboard...
start "Dashboard" cmd /k "cd dashboard && python -m streamlit run dashboard.py"

echo ==========================================
echo ✅ System Started Successfully!
echo ==========================================

pause