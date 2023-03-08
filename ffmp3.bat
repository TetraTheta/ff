@echo off
powershell -File "%~dp0\ff.ps1" mp3 -target "%cd%" %1
exit
