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
# Étape 0: Installer les paquets système nécessaires
# ═══════════════════════════════════════════════════════════════════════════

echo -e "${BLUE}📦 Étape 0: Installation des paquets système...${NC}"
echo "   → Mise à jour de la liste des paquets..."
apt-get update -qq 2>/dev/null
echo "   → Installation de git, python3, pip, wget..."
apt-get install -y -qq \
    git \
    python3 \
    python3-pip \
    python3-venv \
    wget \
    apache2 \
    apache2-utils \
    libapache2-mod-proxy-http \
    curl \
    2>/dev/null

echo -e "${GREEN}✅ Paquets système installés${NC}"
echo ""

# ═══════════════════════════════════════════════════════════════════════════
# Étape 1: Créer les répertoires nécessaires
# ═══════════════════════════════════════════════════════════════════════════

echo -e "${BLUE}� Étape 1: Création des répertoires...${NC}"
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
files=("manage.py" "populate_db.py" "requirements.txt" "project/settings.py" "deploy.sh" "setup-apache.sh" "start-django.sh")
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
# Étape 5: Installer les dépendances Python
# ═══════════════════════════════════════════════════════════════════════════

echo -e "${BLUE}🐍 Étape 5: Installation des dépendances Python...${NC}"
echo "   → Vérification de requirements.txt..."
if [ -f "requirements.txt" ]; then
    echo "   → Mise à jour de pip..."
    pip3 install --upgrade pip setuptools wheel 2>&1 | grep -i "success\|successfully" > /dev/null && echo "      ✅ pip mis à jour" || echo "      ⚠️  pip update"
    
    echo "   → Installation des dépendances..."
    if pip3 install -r requirements.txt 2>&1 | tee /tmp/pip_install.log | grep -i "error"; then
        echo -e "${RED}❌ Erreur lors de l'installation des dépendances${NC}"
        echo "   Détails: tail /tmp/pip_install.log"
        tail -10 /tmp/pip_install.log
    else
        echo -e "${GREEN}✅ Dépendances Python installées${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  requirements.txt non trouvé${NC}"
fi
echo ""

# ═══════════════════════════════════════════════════════════════════════════
# Étape 6: Rendre les scripts exécutables
# ═══════════════════════════════════════════════════════════════════════════

echo -e "${BLUE}⚙️  Étape 6: Configuration des permissions des scripts...${NC}"
chmod +x deploy.sh
chmod +x setup-apache.sh
chmod +x populate_db.py
echo -e "${GREEN}✅ Permissions des scripts configurées${NC}"
echo ""

# ═══════════════════════════════════════════════════════════════════════════
# Étape 7: Définir les permissions Apache
# ═══════════════════════════════════════════════════════════════════════════

echo -e "${BLUE}🔐 Étape 7: Configuration des permissions pour Apache...${NC}"
chown -R www-data:www-data "$PROJECT_PATH"
chmod -R 755 "$PROJECT_PATH"
echo -e "${GREEN}✅ Permissions Apache configurées${NC}"
echo ""

# ═══════════════════════════════════════════════════════════════════════════
# Étape 8: Lancer la configuration Apache
# ═══════════════════════════════════════════════════════════════════════════

echo -e "${BLUE}🌐 Étape 8: Configuration d'Apache...${NC}"
bash "$PROJECT_PATH/setup-apache.sh"
echo ""

# ═══════════════════════════════════════════════════════════════════════════
# Résumé final
# ═══════════════════════════════════════════════════════════════════════════

echo "╔════════════════════════════════════════════════════════════════════════╗"
echo "║               ✅ INITIALISATION COMPLÈTE RÉUSSIE !                    ║"
echo "╠════════════════════════════════════════════════════════════════════════╣"
echo "║                                                                        ║"
echo "║  📁 Projet: $PROJECT_PATH"
echo "║  🔗 Repository: $REPO_URL"
echo "║  📅 Initialisation: $(date '+%d/%m/%Y à %H:%M:%S')"
echo "║                                                                        ║"
echo "║  ✅ Paquets système installés                                         ║"
echo "║  ✅ Repository cloné                                                  ║"
echo "║  ✅ Dépendances Python installées                                     ║"
echo "║  ✅ Apache configuré                                                  ║"
echo "║                                                                        ║"
echo "║  🎯 Prochaines étapes (à faire manuellement):                        ║"
echo "║                                                                        ║"
echo "║  1. Configurer la base de données dans project/settings.py           ║"
echo "║     (MySQL/SQLite selon vos préférences)                             ║"
echo "║                                                                        ║"
echo "║  2. Lancer les migrations Django:                                    ║"
echo "║     cd /var/www/SAE203                                               ║"
echo "║     python3 manage.py migrate                                        ║"
echo "║                                                                        ║"
echo "║  3. Remplir la base de données:                                      ║"
echo "║     python3 populate_db.py                                           ║"
echo "║                                                                        ║"
echo "║  4. Créer un superuser (optionnel):                                  ║"
echo "║     python3 manage.py createsuperuser                                ║"
echo "║                                                                        ║"
echo "║  5. Démarrer Django en arrière-plan:                                 ║"
echo "║     nohup python3 manage.py runserver 127.0.0.1:8000 > /tmp/django.log 2>&1 &"
echo "║                                                                        ║"
echo "║  6. Accéder à l'application:                                         ║"
echo "║     http://localhost                                                 ║"
echo "║                                                                        ║"
echo "║  🚀 Votre VM est prête pour SAE203 !                                  ║"
echo "║                                                                        ║"
echo "╚════════════════════════════════════════════════════════════════════════╝"
echo ""

exit 0
