#!/bin/bash

# ═══════════════════════════════════════════════════════════════════════════
# Script de démarrage Django pour SAE203
# Lance Django en arrière-plan sur le port 8000
# ═══════════════════════════════════════════════════════════════════════════

PROJECT_PATH="/var/www/SAE203"

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo "╔════════════════════════════════════════════════════════════════════════╗"
echo "║        🚀 DÉMARRAGE DJANGO SAE203                                    ║"
echo "╚════════════════════════════════════════════════════════════════════════╝"
echo ""

# Vérifier que le projet existe
echo -e "${BLUE}📂 Vérification du projet...${NC}"
if [ ! -d "$PROJECT_PATH" ]; then
    echo -e "${RED}❌ Le répertoire $PROJECT_PATH n'existe pas${NC}"
    exit 1
fi

cd "$PROJECT_PATH" || exit 1
echo -e "${GREEN}✅ Projet trouvé${NC}"
echo ""

# Arrêter les anciennes instances
echo -e "${BLUE}⏹️  Arrêt des anciennes instances...${NC}"
pkill -f "python3 manage.py runserver" 2>/dev/null || true
sleep 1
echo -e "${GREEN}✅ Prêt${NC}"
echo ""

# Lancer les migrations
echo -e "${BLUE}� Application des migrations...${NC}"
python3 manage.py migrate --noinput 2>&1 | tail -1
echo -e "${GREEN}✅ Migrations appliquées${NC}"
echo ""

# Démarrer Django
echo -e "${BLUE}🚀 Démarrage de Django sur 127.0.0.1:8000...${NC}"
nohup python3 manage.py runserver 127.0.0.1:8000 > /tmp/django.log 2>&1 &
DJANGO_PID=$!
sleep 3

if ps -p $DJANGO_PID > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Django démarré (PID: $DJANGO_PID)${NC}"
else
    echo -e "${RED}❌ Erreur au démarrage${NC}"
    cat /tmp/django.log
    exit 1
fi
echo ""

echo "╔════════════════════════════════════════════════════════════════════════╗"
echo "║               ✅ DJANGO EST EN COURS D'EXÉCUTION !                   ║"
echo "╠════════════════════════════════════════════════════════════════════════╣"
echo "║                                                                        ║"
echo "║  🌐 Accédez à: http://localhost                                       ║"
echo "║  📝 Logs: tail -f /tmp/django.log                                     ║"
echo "║  🛑 Arrêter: pkill -f 'python3 manage.py runserver'                   ║"
echo "║                                                                        ║"
echo "╚════════════════════════════════════════════════════════════════════════╝"
echo ""
