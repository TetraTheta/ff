@echo off
powershell -File "%~dp0\ff.ps1" webpa -target "%cd%" %1
exit
