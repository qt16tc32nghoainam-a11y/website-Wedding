@echo off
rem ============================================================
rem   CONG CU CAP NHAT WEBSITE QUOC AN STUDIO
rem   Nhap dup file nay de mo menu cap nhat.
rem ============================================================
chcp 65001 >nul
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
where python >nul 2>nul
if errorlevel 1 (
  echo.
  echo   Chua cai Python. Tai tai https://www.python.org/downloads/
  echo   ^(nho tick "Add Python to PATH"^), sau do chay lenh:
  echo       python -m pip install pillow numpy
  echo.
  pause
  exit /b
)
python tools\capnhat.py %*
if errorlevel 1 pause
