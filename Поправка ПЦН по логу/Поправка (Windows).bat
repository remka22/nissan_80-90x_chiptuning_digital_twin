@echo off
chcp 65001 >nul
cd /d "%~dp0"

rem --- выбираем чем запускать python ---
set PYEXE=python
where python >nul 2>nul || set PYEXE=py

rem --- запускаем единственный .py в этой папке ---
for %%f in (*.py) do "%PYEXE%" "%%f"

echo.
echo === Готово. Результат в папке "результат ..." рядом. Окно можно закрыть. ===
pause
