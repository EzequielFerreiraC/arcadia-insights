@echo off
REM Arcadia Insights - Setup Script for Windows
REM Gerencia containers Docker e configuração do projeto

setlocal enabledelayedexpansion

:BANNER
cls
echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║                                                            ║
echo ║         ARCADIA INSIGHTS - SETUP MANAGER                   ║
echo ║         Life is Strange Choice Analytics Platform          ║
echo ║                                                            ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

:MENU
echo.
echo MENU PRINCIPAL
echo ═════════════════════════════════════════
echo   1) Iniciar infraestrutura (12 servicos Docker)
echo   2) Parar infraestrutura
echo   3) Reiniciar infraestrutura
echo   4) Ver status dos servicos
echo   5) Ver logs dos servicos
echo   6) Instalar dependencias do backend
echo   7) Instalar dependencias do frontend
echo   8) Iniciar frontend (Next.js)
echo   9) Parar frontend
echo   A) Setup completo (infra + frontend rodando)
echo   C) Limpar tudo (remover containers, volumes, imagens)
echo   0) Sair
echo ═════════════════════════════════════════
echo.

set /p choice="Escolha uma opcao: "

if "%choice%"=="1" goto START_INFRA
if "%choice%"=="2" goto STOP_INFRA
if "%choice%"=="3" goto RESTART_INFRA
if "%choice%"=="4" goto STATUS
if "%choice%"=="5" goto LOGS
if "%choice%"=="6" goto INSTALL_BACKEND
if "%choice%"=="7" goto INSTALL_FRONTEND
if "%choice%"=="8" goto START_FRONTEND
if "%choice%"=="9" goto STOP_FRONTEND
if /i "%choice%"=="A" goto SETUP_ALL
if /i "%choice%"=="C" goto CLEAN_ALL
if "%choice%"=="0" goto EXIT

echo Opcao invalida!
pause
goto BANNER

:START_INFRA
echo.
echo Iniciando infraestrutura...
echo.

REM Verificar se Docker está rodando
docker info >nul 2>&1
if errorlevel 1 (
    echo ERRO: Docker nao esta rodando!
    pause
    goto BANNER
)

REM Criar pastas necessárias
echo Criando pastas necessarias...
if not exist "h_airflow\logs" mkdir h_airflow\logs
if not exist "h_airflow\plugins" mkdir h_airflow\plugins
if not exist "i_ml\trained_models" mkdir i_ml\trained_models
if not exist "logs" mkdir logs

REM Subir containers
echo Iniciando containers (12 servicos)...
docker compose up -d

echo.
echo Aguardando servicos ficarem prontos (20s)...
timeout /t 20 /nobreak >nul

REM Verificar status
echo.
echo Status dos containers:
docker compose ps

echo.
echo [OK] Infraestrutura iniciada com sucesso!
echo.
echo URLs disponiveis:
echo   API Docs:    http://localhost:8000/docs
echo   Frontend:    http://localhost:3000
echo   MinIO:       http://localhost:9001 (arcadia-admin / arcadia-secret-key-123)
echo   Airflow:     http://localhost:8080 (admin / admin)
echo   Prometheus:  http://localhost:9090
echo   Grafana:     http://localhost:3001 (admin / admin)
echo.
pause
goto BANNER

:START_FRONTEND
echo.
echo Iniciando servidor Next.js...
cd d_web

REM Verificar se node_modules existe
if not exist "node_modules" (
    echo Instalando dependencias...
    call npm install
)

REM Matar processo anterior
taskkill /F /IM node.exe /FI "WINDOWTITLE eq Next.js*" >nul 2>&1

REM Iniciar Next.js em nova janela
echo Iniciando Next.js em nova janela...
start "Arcadia Frontend - Next.js" cmd /k "npm run dev"

echo.
echo [OK] Frontend iniciado em nova janela!
echo Aguardando Next.js inicializar (10s)...
timeout /t 10 /nobreak >nul

echo.
echo [OK] Frontend disponivel em: http://localhost:3000
cd ..
pause
goto BANNER

:STOP_FRONTEND
echo.
echo Parando servidor Next.js...
taskkill /F /IM node.exe /FI "WINDOWTITLE eq Arcadia*" >nul 2>&1
taskkill /F /IM node.exe /FI "WINDOWTITLE eq Next.js*" >nul 2>&1
echo [OK] Frontend parado!
pause
goto BANNER

:STOP_INFRA
echo.
echo Parando containers...
docker compose stop
echo [OK] Containers parados!
pause
goto BANNER

:RESTART_INFRA
echo.
echo Reiniciando infraestrutura...
docker compose restart
echo [OK] Containers reiniciados!
pause
goto BANNER

:STATUS
echo.
echo Status dos servicos:
echo.
docker compose ps
echo.
echo Uso de recursos:
docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}"
pause
goto BANNER

:LOGS
echo.
echo Escolha o servico para ver logs:
echo   1) PostgreSQL
echo   2) Redis
echo   3) Kafka
echo   4) Airflow Webserver
echo   5) MinIO
echo   6) Todos
set /p service_choice="Opcao: "

if "%service_choice%"=="1" docker compose logs -f postgres
if "%service_choice%"=="2" docker compose logs -f redis
if "%service_choice%"=="3" docker compose logs -f kafka
if "%service_choice%"=="4" docker compose logs -f airflow-webserver
if "%service_choice%"=="5" docker compose logs -f minio
if "%service_choice%"=="6" docker compose logs -f

pause
goto BANNER

:INSTALL_BACKEND
echo.
echo Instalando dependencias do backend...
cd c_api

if not exist ".venv" (
    echo Criando ambiente virtual...
    python -m venv .venv
)

echo Instalando pacotes Python...
call .venv\Scripts\activate.bat
pip install -e ".[dev]"

echo [OK] Backend configurado!
echo Para rodar: cd c_api ^&^& .venv\Scripts\activate ^&^& uvicorn src.main:app --reload
cd ..
pause
goto BANNER

:INSTALL_FRONTEND
echo.
echo Instalando dependencias do frontend...
cd d_web

echo Instalando pacotes Node.js...
call npm install

echo [OK] Frontend configurado!
echo Para rodar: cd d_web ^&^& npm run dev
cd ..
pause
goto BANNER

:SETUP_ALL
echo.
echo Configuracao completa do projeto
echo.

REM Criar pasta de logs
if not exist "logs" mkdir logs

REM Iniciar infraestrutura
call :START_INFRA_SILENT

REM Instalar frontend
echo.
call :INSTALL_FRONTEND_SILENT

REM Iniciar frontend
echo.
cd d_web
echo Iniciando Next.js em nova janela...
start "Arcadia Frontend - Next.js" cmd /k "npm run dev"
cd ..

echo.
echo Aguardando Next.js inicializar (10s)...
timeout /t 10 /nobreak >nul

echo.
echo ════════════════════════════════════════
echo Setup completo finalizado!
echo ════════════════════════════════════════
echo.
echo Acesse o frontend em: http://localhost:3000
echo.
pause
goto BANNER

:START_INFRA_SILENT
echo Iniciando infraestrutura...
docker info >nul 2>&1
if errorlevel 1 (
    echo ERRO: Docker nao esta rodando!
    exit /b 1
)
if not exist "h_airflow\logs" mkdir h_airflow\logs
if not exist "h_airflow\plugins" mkdir h_airflow\plugins
if not exist "i_ml\trained_models" mkdir i_ml\trained_models
docker compose up -d >nul 2>&1
echo Aguardando servicos (20s)...
timeout /t 20 /nobreak >nul
echo [OK] Infraestrutura iniciada!
exit /b 0

:INSTALL_FRONTEND_SILENT
cd d_web
if not exist "node_modules" (
    echo Instalando dependencias do frontend...
    call npm install >nul 2>&1
    echo [OK] Dependencias instaladas!
) else (
    echo Dependencias ja instaladas.
)
cd ..
exit /b 0

:CLEAN_ALL
echo.
echo AVISO: Isso ira remover TODOS os containers, volumes e imagens!
echo Todos os dados serao perdidos!
set /p confirm="Tem certeza? (digite 'sim' para confirmar): "

if /i not "%confirm%"=="sim" (
    echo Operacao cancelada.
    pause
    goto BANNER
)

echo Parando e removendo containers...
docker compose down -v

echo Removendo imagens do projeto...
for /f "tokens=3" %%i in ('docker images ^| findstr arcadia') do (
    docker rmi -f %%i 2>nul
)

echo Limpando pastas de dados...
if exist "h_airflow\logs" rmdir /s /q h_airflow\logs
if exist "h_airflow\plugins" rmdir /s /q h_airflow\plugins
if exist "i_ml\trained_models" rmdir /s /q i_ml\trained_models

echo [OK] Limpeza completa realizada!
pause
goto BANNER

:EXIT
echo.
echo Saindo...
exit /b 0
