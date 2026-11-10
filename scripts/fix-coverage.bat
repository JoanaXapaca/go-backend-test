@echo off
powershell -NoProfile -ExecutionPolicy Bypass -Command "(Get-Content coverage.xml) -replace '\\', '/' | Set-Content coverage.xml"