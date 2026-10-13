@echo off
cd /d "%~dp0"

REM 1) Instalar uv si no existe
where uv >nul 2>nul || powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
set "PATH=%USERPROFILE%\.local\bin;%PATH%"

REM 2) Crear el entorno solo la primera vez (uv descarga Python si hace falta)
if not exist .venv uv venv .venv --python 3.12

REM 3) Instalar o actualizar dependencias (rápido si ya están)
uv pip install --link-mode=copy -r requirements.txt

REM 4) Ejecutar sin activar el venv
REM Uso: run.bat "03 March" "C:\logistic-control"
set "MES=%~1"
set "RUTA=%~2"

if "%MES%"=="" set /p "MES=Mes (ej. 03 March): "
if "%RUTA%"=="" set /p "RUTA=Ruta de carpeta Unilever (SharePoint): "

REM Quitar la \ final (si no, rompe las comillas al pasarla a Python)
if defined RUTA if "%RUTA:~-1%"=="\" set "RUTA=%RUTA:~0,-1%"

if "%RUTA%"=="" (
    .venv\Scripts\python.exe main.py --month "%MES%"
) else (
    .venv\Scripts\python.exe main.py --month "%MES%" --unilever_path "%RUTA%"
)
pause