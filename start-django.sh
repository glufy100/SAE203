#!/bin/bash

# ═══════════════════════════════════════════════════════════════════════════
# Script de démarrage Django pour SAE203
# Lance Django en arrière-plan et teste la connexion
# ═══════════════════════════════════════════════════════════════════════════

set +e

echo "╔════════════════════════════════════════════════════════════════════════╗"
echo "║        🚀 DÉMARRAGE DJANGO SAE203                                    ║"
echo "╚════════════════════════════════════════════════════════════════════════╝"
echo ""

# Configuration
PROJECT_PATH="/var/www/SAE203"

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# ═══════════════════════════════════════════════════════════════════════════
# Étape 1: Vérifier que le projet existe
# ═══════════════════════════════════════════════════════════════════════════

echo -e "${BLUE}📂 Étape 1: Vérification du projet...${NC}"
if [ ! -d "$PROJECT_PATH" ]; then
    echo -e "${RED}❌ Le répertoire $PROJECT_PATH n'existe pas${NC}"
    echo -e "${YELLOW}   Exécutez d'abord: sudo ./init-vm.sh${NC}"
    exit 1
fi
cd "$PROJECT_PATH" || exit 1
echo -e "${GREEN}✅ Projet trouvé: $PROJECT_PATH${NC}"
echo ""

# ═══════════════════════════════════════════════════════════════════════════
# Étape 2: Vérifier les migrations
# ═══════════════════════════════════════════════════════════════════════════

echo -e "${BLUE}🔄 Étape 2: Lancer les migrations Django...${NC}"
if ! python3 manage.py migrate 2>&1 | grep -q "error\|Error"; then
    echo -e "${GREEN}✅ Migrations appliquées${NC}"
else
    echo -e "${YELLOW}⚠️  Vérifiez la configuration de la base de données${NC}"
fi
echo ""

# ═══════════════════════════════════════════════════════════════════════════
# Étape 3: Remplir la base de données
# ═══════════════════════════════════════════════════════════════════════════

echo -e "${BLUE}📊 Étape 3: Remplissage de la base de données...${NC}"
echo "   → Vous pouvez exécuter ceci manuellement plus tard avec:"
echo "      python3 populate_db.py"
echo ""

# ═══════════════════════════════════════════════════════════════════════════
# Étape 4: Arrêter les anciennes instances Django
# ═══════════════════════════════════════════════════════════════════════════

echo -e "${BLUE}⏹️  Étape 4: Arrêt des anciennes instances Django...${NC}"
pkill -f "python3 manage.py runserver" 2>/dev/null || true
sleep 2
echo -e "${GREEN}✅ Anciennes instances arrêtées${NC}"
echo ""

# ═══════════════════════════════════════════════════════════════════════════
# Étape 5: Lancer Django en arrière-plan
# ═══════════════════════════════════════════════════════════════════════════

echo -e "${BLUE}🚀 Étape 5: Démarrage de Django...${NC}"
nohup python3 manage.py runserver 127.0.0.1:8000 > /tmp/django.log 2>&1 &
DJANGO_PID=$!
echo "   → PID: $DJANGO_PID"
sleep 3

# Vérifier que Django a démarré
if ps -p $DJANGO_PID > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Django démarré avec succès${NC}"
else
    echo -e "${RED}❌ Erreur lors du démarrage de Django${NC}"
    echo "   Vérifiez les logs: cat /tmp/django.log"
    tail -20 /tmp/django.log
    exit 1
fi
echo ""

# ═══════════════════════════════════════════════════════════════════════════
# Étape 6: Tester la connexion
# ═══════════════════════════════════════════════════════════════════════════

echo -e "${BLUE}🧪 Étape 6: Test de la connexion...${NC}"
sleep 2
if curl -s http://127.0.0.1:8000/ > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Django répond correctement${NC}"
else
    echo -e "${YELLOW}⚠️  Django n'a pas répondu (peut prendre quelques secondes)${NC}"
fi
echo ""

# ═══════════════════════════════════════════════════════════════════════════
# Résumé final
# ═══════════════════════════════════════════════════════════════════════════

echo "╔════════════════════════════════════════════════════════════════════════╗"
echo "║               ✅ DÉMARRAGE DJANGO RÉUSSI !                           ║"
echo "╠════════════════════════════════════════════════════════════════════════╣"
echo "║                                                                        ║"
echo "║  🐍 Django: ✅ En cours d'exécution sur 127.0.0.1:8000               ║"
echo "║  📁 Projet: $PROJECT_PATH"
echo "║  📅 Heure: $(date '+%d/%m/%Y à %H:%M:%S')"
echo "║                                                                        ║"
echo "║  🎯 Accès à l'application:                                           ║"
echo "║                                                                        ║"
echo "║  → http://localhost                                                  ║"
echo "║  → http://sae203.local                                               ║"
echo "║                                                                        ║"
echo "║  📝 Logs Django:                                                      ║"
echo "║  → tail -f /tmp/django.log                                           ║"
echo "║                                                                        ║"
echo "║  🛑 Arrêter Django:                                                   ║"
echo "║  → pkill -f 'python3 manage.py runserver'                            ║"
echo "║                                                                        ║"
echo "║  🔄 Redémarrer Django:                                               ║"
echo "║  → sudo ./start-django.sh                                            ║"
echo "║                                                                        ║"
echo "╚════════════════════════════════════════════════════════════════════════╝"
echo ""

exit 0
