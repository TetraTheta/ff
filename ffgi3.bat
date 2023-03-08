@echo off
powershell -File "%~dp0\ff.ps1" gi -target "%cd%" -giType 3 -width 1280 %1
exit
