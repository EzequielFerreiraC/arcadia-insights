#!/bin/bash

# Arcadia Insights - Setup Script
# Gerencia containers Docker e configuração do projeto

set -e

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

# Detecta se esta rodando no Git Bash/MSYS (Windows) em vez de WSL/Linux nativo.
# O npm do Windows corrompe node_modules sobre o filesystem 9P do WSL (erros EISDIR),
# entao sempre roteamos npm para dentro do WSL quando estamos no Git Bash.
case "$(uname -s)" in
  MINGW*|MSYS*|CYGWIN*) IS_WIN_BASH=true ;;
  *) IS_WIN_BASH=false ;;
esac
WSL_DISTRO="ubuntu-llm"
WSL_PROJECT_DIR="/home/efcardoso/projects/arcadia-insights"

# Executa npm sempre com o npm nativo do Linux.
run_npm() {
    if [ "$IS_WIN_BASH" = true ]; then
        wsl -d "$WSL_DISTRO" bash -lc "cd '$WSL_PROJECT_DIR/d_web' && npm $*"
    else
        ( cd d_web && npm "$@" )
    fi
}

# Banner
echo -e "${MAGENTA}"
echo "╔════════════════════════════════════════════════════════════╗"
echo "║                                                            ║"
echo "║         ARCADIA INSIGHTS - SETUP MANAGER                   ║"
echo "║         Life is Strange Choice Analytics Platform          ║"
echo "║                                                            ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Funções
start_infrastructure() {
    echo -e "${CYAN}Iniciando infraestrutura...${NC}"
    echo ""
    
    # Verificar se Docker está rodando
    if ! docker info > /dev/null 2>&1; then
        echo -e "${RED}Erro: Docker não está rodando!${NC}"
        exit 1
    fi
    
    # Criar pastas necessárias
    echo -e "${YELLOW}Criando pastas necessárias...${NC}"
    mkdir -p h_airflow/logs h_airflow/plugins
    mkdir -p i_ml/trained_models
    
    # Subir containers
    echo -e "${YELLOW}Iniciando containers (12 serviços)...${NC}"
    docker compose up -d
    
    echo ""
    echo -e "${GREEN}Aguardando serviços ficarem prontos (20s)...${NC}"
    sleep 20
    
    # Verificar status
    echo ""
    echo -e "${CYAN}Status dos containers:${NC}"
    docker compose ps
    
    echo ""
    echo -e "${GREEN}✓ Infraestrutura iniciada com sucesso!${NC}"
    echo ""
    echo -e "${CYAN}URLs disponíveis:${NC}"
    echo -e "  ${WHITE}API Docs:    ${GREEN}http://localhost:8000/docs${NC}"
    echo -e "  ${WHITE}Frontend:    ${GREEN}http://localhost:3000${NC}"
    echo -e "  ${WHITE}MinIO:       ${GREEN}http://localhost:9001${NC} (arcadia-admin / arcadia-secret-key-123)"
    echo -e "  ${WHITE}Airflow:     ${GREEN}http://localhost:8080${NC} (admin / admin)"
    echo -e "  ${WHITE}Prometheus:  ${GREEN}http://localhost:9090${NC}"
    echo -e "  ${WHITE}Grafana:     ${GREEN}http://localhost:3001${NC} (admin / admin)"
    echo ""
}

start_frontend() {
    echo -e "${CYAN}Iniciando servidor Next.js...${NC}"
    mkdir -p logs

    # Garante dependencias instaladas (npm nativo do Linux)
    if [ "$IS_WIN_BASH" = true ]; then
        if ! wsl -d "$WSL_DISTRO" bash -lc "test -d '$WSL_PROJECT_DIR/d_web/node_modules'"; then
            echo -e "${YELLOW}Instalando dependências...${NC}"
            run_npm install
        fi
        # Mata processo anterior e inicia totalmente destacado dentro do WSL
        wsl -d "$WSL_DISTRO" bash -lc "pkill -f 'next dev' 2>/dev/null || true"
        echo -e "${YELLOW}Iniciando Next.js em background (WSL)...${NC}"
        wsl -d "$WSL_DISTRO" bash -lc "cd '$WSL_PROJECT_DIR/d_web' && setsid nohup npm run dev > '$WSL_PROJECT_DIR/logs/frontend.log' 2>&1 < /dev/null &"
    else
        cd d_web
        if [ ! -d "node_modules" ]; then
            echo -e "${YELLOW}Instalando dependências...${NC}"
            npm install
        fi
        pkill -f "next dev" 2>/dev/null || true
        echo -e "${YELLOW}Iniciando Next.js em background...${NC}"
        setsid nohup npm run dev > ../logs/frontend.log 2>&1 < /dev/null &
        cd ..
    fi

    echo ""
    echo -e "${CYAN}Aguardando Next.js inicializar (10s)...${NC}"
    sleep 10
    echo -e "${GREEN}✓ Frontend disponível em: ${WHITE}http://localhost:3000${NC}"
    echo -e "${CYAN}Logs em: ${WHITE}logs/frontend.log${NC}"
}

stop_frontend() {
    echo -e "${YELLOW}Parando servidor Next.js...${NC}"
    pkill -f "next dev" 2>/dev/null || true
    echo -e "${GREEN}✓ Frontend parado!${NC}"
}

stop_infrastructure() {
    echo -e "${YELLOW}Parando containers...${NC}"
    docker compose stop
    echo -e "${GREEN}✓ Containers parados!${NC}"
}

clean_infrastructure() {
    echo -e "${RED}AVISO: Isso irá remover TODOS os containers, volumes e imagens!${NC}"
    echo -e "${YELLOW}Todos os dados serão perdidos!${NC}"
    read -p "Tem certeza? (digite 'sim' para confirmar): " confirm
    
    if [ "$confirm" = "sim" ]; then
        echo -e "${YELLOW}Parando e removendo containers...${NC}"
        docker compose down -v
        
        echo -e "${YELLOW}Removendo imagens do projeto...${NC}"
        docker images | grep arcadia | awk '{print $3}' | xargs -r docker rmi -f 2>/dev/null || true
        
        # Remover pastas de dados
        echo -e "${YELLOW}Limpando pastas de dados...${NC}"
        rm -rf h_airflow/logs/* h_airflow/plugins/* 2>/dev/null || true
        rm -rf i_ml/trained_models/* 2>/dev/null || true
        
        echo -e "${GREEN}✓ Limpeza completa realizada!${NC}"
    else
        echo -e "${CYAN}Operação cancelada.${NC}"
    fi
}

restart_infrastructure() {
    echo -e "${CYAN}Reiniciando infraestrutura...${NC}"
    docker compose restart
    echo -e "${GREEN}✓ Containers reiniciados!${NC}"
}

show_status() {
    echo -e "${CYAN}Status dos serviços:${NC}"
    echo ""
    docker compose ps
    echo ""
    
    echo -e "${CYAN}Uso de recursos:${NC}"
    docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}" | head -n 13
}

show_logs() {
    echo -e "${CYAN}Escolha o serviço para ver logs:${NC}"
    echo "  1) PostgreSQL"
    echo "  2) Redis"
    echo "  3) Kafka"
    echo "  4) Airflow Webserver"
    echo "  5) MinIO"
    echo "  6) Todos"
    read -p "Opção: " service_choice
    
    case $service_choice in
        1) docker compose logs -f postgres ;;
        2) docker compose logs -f redis ;;
        3) docker compose logs -f kafka ;;
        4) docker compose logs -f airflow-webserver ;;
        5) docker compose logs -f minio ;;
        6) docker compose logs -f ;;
        *) echo -e "${RED}Opção inválida!${NC}" ;;
    esac
}

install_backend() {
    echo -e "${CYAN}Instalando dependências do backend...${NC}"
    cd c_api
    
    if [ ! -d ".venv" ]; then
        echo -e "${YELLOW}Criando ambiente virtual...${NC}"
        python3 -m venv .venv
    fi
    
    echo -e "${YELLOW}Instalando pacotes Python...${NC}"
    source .venv/bin/activate
    pip install -e ".[dev]"
    
    echo -e "${GREEN}✓ Backend configurado!${NC}"
    echo -e "${CYAN}Para rodar: ${WHITE}cd c_api && source .venv/bin/activate && uvicorn src.main:app --reload${NC}"
    cd ..
}

install_frontend() {
    echo -e "${CYAN}Instalando dependências do frontend...${NC}"
    echo -e "${YELLOW}Instalando pacotes Node.js (via WSL)...${NC}"
    run_npm install

    echo -e "${GREEN}✓ Frontend configurado!${NC}"
    echo -e "${CYAN}Para rodar: ${WHITE}opção 8 do menu${NC}"
}

setup_all() {
    echo -e "${MAGENTA}Configuração completa do projeto${NC}"
    echo ""
    
    # Criar pasta de logs
    mkdir -p logs
    
    # Iniciar infraestrutura
    start_infrastructure
    
    # Instalar frontend
    echo ""
    install_frontend
    
    # Iniciar frontend
    echo ""
    start_frontend
    
    echo ""
    echo -e "${GREEN}════════════════════════════════════════${NC}"
    echo -e "${GREEN}Setup completo finalizado!${NC}"
    echo -e "${GREEN}════════════════════════════════════════${NC}"
    echo ""
    echo -e "${CYAN}Acesse o frontend em: ${WHITE}http://localhost:3000${NC}"
    echo ""
}

# Menu principal
show_menu() {
    echo ""
    echo -e "${CYAN}MENU PRINCIPAL${NC}"
    echo -e "${CYAN}═════════════════════════════════════════${NC}"
    echo -e "  ${GREEN}1)${NC} Iniciar infraestrutura (12 serviços Docker)"
    echo -e "  ${GREEN}2)${NC} Parar infraestrutura"
    echo -e "  ${GREEN}3)${NC} Reiniciar infraestrutura"
    echo -e "  ${GREEN}4)${NC} Ver status dos serviços"
    echo -e "  ${GREEN}5)${NC} Ver logs dos serviços"
    echo -e "  ${GREEN}6)${NC} Instalar dependências do backend"
    echo -e "  ${GREEN}7)${NC} Instalar dependências do frontend"
    echo -e "  ${GREEN}8)${NC} Iniciar frontend (Next.js)"
    echo -e "  ${GREEN}9)${NC} Parar frontend"
    echo -e "  ${GREEN}A)${NC} Setup completo (infra + frontend rodando)"
    echo -e "  ${RED}C)${NC} Limpar tudo (remover containers, volumes, imagens)"
    echo -e "  ${YELLOW}0)${NC} Sair"
    echo -e "${CYAN}═════════════════════════════════════════${NC}"
    echo ""
}

# Loop principal
while true; do
    show_menu
    read -p "Escolha uma opção: " choice
    
    case $choice in
        1) start_infrastructure ;;
        2) stop_infrastructure ;;
        3) restart_infrastructure ;;
        4) show_status ;;
        5) show_logs ;;
        6) install_backend ;;
        7) install_frontend ;;
        8) start_frontend ;;
        9) stop_frontend ;;
        [aA]) setup_all ;;
        [cC]) clean_infrastructure ;;
        0) 
            echo -e "${CYAN}Saindo...${NC}"
            exit 0
            ;;
        *) 
            echo -e "${RED}Opção inválida!${NC}"
            ;;
    esac
    
    echo ""
    read -p "Pressione Enter para continuar..."
done
