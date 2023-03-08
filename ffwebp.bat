@echo off
powershell -File "%~dp0\ff.ps1" webp -target "%cd%" %1
pause
