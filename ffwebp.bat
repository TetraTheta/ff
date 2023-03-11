@echo off
if [%1]==[] (python %~dp0\ff.py webp) else (python %~dp0\ff.py webp %1)
