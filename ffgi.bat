@echo off
if [%1]==[] (python %~dp0\ff.py gi --type 0) else (python %~dp0\ff.py gi --type 0 %1)
