@echo off
powershell -File "%~dp0\ff.ps1" webm -target "%cd%" %1
exit
