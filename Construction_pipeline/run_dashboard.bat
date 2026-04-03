@echo off
echo 📊 Starting Dashboard...

cd /d %~dp0

python -m streamlit run dashboard/dashboard.py

pause