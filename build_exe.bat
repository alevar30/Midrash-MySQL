@echo off
echo ============================================
echo  Midrash - Compilar a EXE
echo ============================================
echo.

:: Verificar que PyInstaller está instalado
pip show pyinstaller >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Instalando PyInstaller...
    pip install pyinstaller
    echo.
)

:: Limpiar compilaciones anteriores
if exist "dist" rmdir /s /q dist
if exist "build" rmdir /s /q build
if exist "Midrash.spec" del /q Midrash.spec

echo Compilando Midrash.exe...
echo.

pyinstaller --noconfirm --onefile --windowed ^
    --name "Midrash" ^
    --add-data "assets;assets" ^
    --add-data "database;database" ^
    --add-data "gui;gui" ^
    --icon "assets/logo.png" ^
    main.py

echo.
if exist "dist\Midrash.exe" (
    echo ============================================
    echo  COMPILACION EXITOSA
    echo  El archivo esta en: dist\Midrash.exe
    echo ============================================
) else (
    echo ============================================
    echo  ERROR: No se pudo compilar el EXE
    echo  Revisa los mensajes de arriba
    echo ============================================
)

echo.
pause
