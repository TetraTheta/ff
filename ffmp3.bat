@echo off
if [%1]==[] (python %~dp0\ff.py mp3) else (python %~dp0\ff.py mp3 %1)
