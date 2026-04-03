@echo off
echo 🚀 Starting Data Pipeline...

cd /d %~dp0

REM Activate virtual environment (if you have one)
REM call venv\Scripts\activate

cd code

python main.py

pause