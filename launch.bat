@echo off
start cmd /k "cd /d %~dp0 && python app_server.py"
start "" http://127.0.0.1:5000/