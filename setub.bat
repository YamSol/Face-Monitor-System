@echo off
echo ========================================
echo  Configurando Sistema de Monitoramento
echo ========================================

echo Instalando dependências...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo Erro na instalação das dependências!
    pause
    exit /b 1
)

echo.
echo Configurando para iniciar com o Windows...
python face_monitor.py --setup-startup

if %errorlevel% neq 0 (
    echo Erro na configuração do startup!
    pause
    exit /b 1
)

echo.
echo ========================================
echo  Configuração concluída com sucesso!
echo ========================================
echo.
echo O sistema está pronto para uso.
echo Para iniciar manualmente: python face_monitor.py
echo Para remover do startup: execute uninstall.bat
echo.
pause