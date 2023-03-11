@echo off
if [%1]==[] (python %~dp0\ff.py gi --type 3) else (python %~dp0\ff.py gi --type 3 %1)
