@echo off
if [%1]==[] (python %~dp0\ff.py webm) else (python %~dp0\ff.py webm %1)
