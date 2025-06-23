@echo off
echo ========================================
echo  Iniciação Manual do Sistema de Monitoramento
echo ========================================


echo.
echo Iniciando Sistema...
python face_monitor.py

if %errorlevel% neq 0 (
    echo Erro ao iniciar sistema manualmente!
    pause
    exit /b 1
)