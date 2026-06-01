#!/bin/bash

# ═══════════════════════════════════════════════════════════════════════════
# Script d'initialisation SAE203 - Nouvelle VM Debian
# Clone le repository, crée les répertoires et configure tout
# ═══════════════════════════════════════════════════════════════════════════

set +e

echo "╔════════════════════════════════════════════════════════════════════════╗"
echo "║        🚀 INITIALISATION SAE203 - NOUVELLE VM DEBIAN                  ║"
echo "╚════════════════════════════════════════════════════════════════════════╝"
echo ""

# Configuration
BASE_PATH="/var/www"
PROJECT_PATH="/var/www/SAE203"
REPO_URL="https://github.com/glufy100/SAE203.git"

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Vérifier que le script s'exécute en tant que root
if [ "$EUID" -ne 0 ]; then 
    echo -e "${RED}❌ Ce script doit être exécuté avec sudo${NC}"
    exit 1
fi

# ═══════════════════════════════════════════════════════════════════════════
# Étape 1: Créer les répertoires nécessaires
# ═══════════════════════════════════════════════════════════════════════════

echo -e "${BLUE}📦 Étape 1: Création des répertoires...${NC}"
if [ -d "$PROJECT_PATH" ]; then
    echo -e "${YELLOW}⚠️  Le répertoire $PROJECT_PATH existe déjà${NC}"
    echo -e "${YELLOW}   Suppression de l'ancien répertoire...${NC}"
    rm -rf "$PROJECT_PATH"
fi

mkdir -p "$BASE_PATH"
echo -e "${GREEN}✅ Répertoire créé: $BASE_PATH${NC}"
echo ""

# ═══════════════════════════════════════════════════════════════════════════
# Étape 2: Cloner le repository
# ═══════════════════════════════════════════════════════════════════════════

echo -e "${BLUE}🔄 Étape 2: Clonage du repository...${NC}"
echo "   → $REPO_URL"
cd "$BASE_PATH" || exit 1
if git clone "$REPO_URL" 2>&1 | grep -q "fatal"; then
    echo -e "${RED}❌ Erreur lors du clonage du repository${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Repository cloné avec succès${NC}"
echo ""

# ═══════════════════════════════════════════════════════════════════════════
# Étape 3: Configurer Git (safe.directory)
# ═══════════════════════════════════════════════════════════════════════════

echo -e "${BLUE}📦 Étape 3: Configuration de Git...${NC}"
git config --global --add safe.directory "$PROJECT_PATH" 2>/dev/null || true
echo -e "${GREEN}✅ Git configuré${NC}"
echo ""

# ═══════════════════════════════════════════════════════════════════════════
# Étape 4: Vérifier les fichiers
# ═══════════════════════════════════════════════════════════════════════════

echo -e "${BLUE}🔍 Étape 4: Vérification des fichiers...${NC}"
cd "$PROJECT_PATH" || exit 1
files=("manage.py" "populate_db.py" "requirements.txt" "project/settings.py" "deploy.sh")
all_ok=true
for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo -e "   ${GREEN}✅ $file${NC}"
    else
        echo -e "   ${RED}❌ $file (MANQUANT)${NC}"
        all_ok=false
    fi
done
echo ""

if [ "$all_ok" = false ]; then
    echo -e "${RED}❌ Certains fichiers sont manquants!${NC}"
    exit 1
fi

# ═══════════════════════════════════════════════════════════════════════════
# Étape 5: Rendre les scripts exécutables
# ═══════════════════════════════════════════════════════════════════════════

echo -e "${BLUE}⚙️  Étape 5: Configuration des permissions...${NC}"
chmod +x deploy.sh
chmod +x populate_db.py
echo -e "${GREEN}✅ Permissions configurées${NC}"
echo ""

# ═══════════════════════════════════════════════════════════════════════════
# Étape 6: Définir les permissions Apache
# ═══════════════════════════════════════════════════════════════════════════

echo -e "${BLUE}🔐 Étape 6: Configuration des permissions pour Apache...${NC}"
chown -R www-data:www-data "$PROJECT_PATH"
chmod -R 755 "$PROJECT_PATH"
echo -e "${GREEN}✅ Permissions Apache configurées${NC}"
echo ""

# ═══════════════════════════════════════════════════════════════════════════
# Étape 7: Redémarrer Apache
# ═══════════════════════════════════════════════════════════════════════════

echo -e "${BLUE}🌐 Étape 7: Démarrage d'Apache...${NC}"
if ! systemctl restart apache2; then
    echo -e "${YELLOW}⚠️  Apache n'est pas installé, installation recommandée${NC}"
else
    sleep 2
    if systemctl is-active --quiet apache2; then
        echo -e "${GREEN}✅ Apache démarré avec succès${NC}"
    else
        echo -e "${RED}❌ Apache n'a pas pu être démarré${NC}"
    fi
fi
echo ""

# ═══════════════════════════════════════════════════════════════════════════
# Résumé final
# ═══════════════════════════════════════════════════════════════════════════

echo "╔════════════════════════════════════════════════════════════════════════╗"
echo "║               ✅ INITIALISATION RÉUSSIE !                            ║"
echo "╠════════════════════════════════════════════════════════════════════════╣"
echo "║                                                                        ║"
echo "║  📁 Projet: $PROJECT_PATH"
echo "║  🔗 Repository: $REPO_URL"
echo "║  📅 Initialisation: $(date '+%d/%m/%Y à %H:%M:%S')"
echo "║                                                                        ║"
echo "║  🎯 Prochaines étapes:                                               ║"
echo "║                                                                        ║"
echo "║  1. Configurer la base de données dans project/settings.py           ║"
echo "║  2. Lancer les migrations Django:                                    ║"
echo "║     python manage.py migrate                                         ║"
echo "║                                                                        ║"
echo "║  3. Remplir la base de données:                                      ║"
echo "║     python populate_db.py                                            ║"
echo "║                                                                        ║"
echo "║  4. Pour les mises à jour ultérieures, utiliser:                    ║"
echo "║     sudo ./deploy.sh                                                 ║"
echo "║                                                                        ║"
echo "║  Votre VM est maintenant prête ! 🚀                                   ║"
echo "║                                                                        ║"
echo "╚════════════════════════════════════════════════════════════════════════╝"
echo ""

exit 0
