@echo off
if [%1]==[] (python %~dp0\ff.py webpa) else (python %~dp0\ff.py webpa %1)
exit
