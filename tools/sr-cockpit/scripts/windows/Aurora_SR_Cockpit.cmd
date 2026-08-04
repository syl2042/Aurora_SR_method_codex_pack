@echo off
setlocal

set "SCRIPT_DIR=%~dp0"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%SCRIPT_DIR%Aurora_SR_Cockpit.ps1"

echo.
echo Appuie sur une touche pour fermer cette fenetre.
pause >nul
