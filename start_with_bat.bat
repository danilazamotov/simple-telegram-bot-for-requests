@echo off
cd /d "%~dp0"
echo Path: %~dp0
python -m venv venv
timeout /t 10 /nobreak > nul
call venv\Scripts\activate
pip install -r requirements.txt
python run.py
pause