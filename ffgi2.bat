@echo off
if [%1]==[] (python %~dp0\ff.py gi --type 2) else (python %~dp0\ff.py gi --type 2 %1)
exit
