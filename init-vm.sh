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
apt-get update -qq 2>/dev/null || apt-get update

echo "   → Installation de git, python3, pip, wget, curl, apache2..."
apt-get install -y -qq \
    git \
    python3 \
    python3-pip \
    python3-venv \
    wget \
    curl \
    apache2 \
    apache2-utils \
    libapache2-mod-proxy-http \
    2>/dev/null

# Vérifier que git est bien installé
if ! command -v git &> /dev/null; then
    echo -e "${RED}❌ git n'a pas pu être installé${NC}"
    exit 1
fi

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

# Cloner le repository
git clone "$REPO_URL" 2>&1
echo -e "${GREEN}✅ Commande de clone exécutée${NC}"
echo ""

# ═══════════════════════════════════════════════════════════════════════════
# Étape 3: Vérifier que le clone a fonctionné
# ═══════════════════════════════════════════════════════════════════════════

echo -e "${BLUE}� Étape 3: Vérification du clone...${NC}"

if [ ! -d "$PROJECT_PATH" ]; then
    echo -e "${RED}❌ ERREUR: Le répertoire $PROJECT_PATH n'existe pas!${NC}"
    echo ""
    echo "📋 DIAGNOSTIC:"
    echo "   Contenu de $BASE_PATH:"
    ls -la "$BASE_PATH"
    echo ""
    echo "   Commandes à essayer manuellement:"
    echo "   1. cd /var/www"
    echo "   2. git clone https://github.com/glufy100/SAE203.git"
    echo "   3. cd SAE203"
    echo "   4. ls -la"
    echo ""
    exit 1
fi

echo -e "${GREEN}✅ Répertoire trouvé${NC}"
echo ""

# Accéder au répertoire
cd "$PROJECT_PATH" || {
    echo -e "${RED}❌ Impossible d'accéder à $PROJECT_PATH${NC}"
    exit 1
}

echo -e "${GREEN}✅ Répertoire accessible: $(pwd)${NC}"
echo ""

# ═══════════════════════════════════════════════════════════════════════════
# Étape 4: Configurer Git (safe.directory)
# ═══════════════════════════════════════════════════════════════════════════

echo -e "${BLUE}📦 Étape 4: Configuration de Git...${NC}"
git config --global --add safe.directory "$PROJECT_PATH" 2>/dev/null || true
echo -e "${GREEN}✅ Git configuré${NC}"
echo ""

# ═══════════════════════════════════════════════════════════════════════════
# Étape 5: Vérifier les fichiers
# ═══════════════════════════════════════════════════════════════════════════

echo -e "${BLUE}🔍 Étape 5: Vérification des fichiers...${NC}"
files=("manage.py" "populate_db.py" "requirements.txt" "project/settings.py" "deploy.sh" "setup-apache.sh")
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
# Étape 6: Installer les dépendances Python
# ═══════════════════════════════════════════════════════════════════════════

echo -e "${BLUE}🐍 Étape 6: Installation des dépendances Python...${NC}"
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
# Étape 7: Rendre les scripts exécutables
# ═══════════════════════════════════════════════════════════════════════════

echo -e "${BLUE}⚙️  Étape 7: Configuration des permissions des scripts...${NC}"
chmod +x deploy.sh 2>/dev/null || true
chmod +x setup-apache.sh 2>/dev/null || true
chmod +x start-django.sh 2>/dev/null || true
chmod +x populate_db.py 2>/dev/null || true
echo -e "${GREEN}✅ Permissions des scripts configurées${NC}"
echo ""

# ═══════════════════════════════════════════════════════════════════════════
# Étape 8: Définir les permissions Apache
# ═══════════════════════════════════════════════════════════════════════════

echo -e "${BLUE}🔐 Étape 8: Configuration des permissions pour Apache...${NC}"
chown -R www-data:www-data "$PROJECT_PATH" 2>/dev/null || true
chmod -R 755 "$PROJECT_PATH" 2>/dev/null || true
echo -e "${GREEN}✅ Permissions Apache configurées${NC}"
echo ""

# ═══════════════════════════════════════════════════════════════════════════
# Étape 9: Vérifier Apache
# ═══════════════════════════════════════════════════════════════════════════

echo -e "${BLUE}🌐 Étape 9: Vérification d'Apache...${NC}"
if systemctl is-active --quiet apache2; then
    echo -e "${GREEN}✅ Apache est en cours d'exécution${NC}"
else
    echo -e "${YELLOW}⚠️  Tentative de démarrage d'Apache...${NC}"
    systemctl start apache2 2>/dev/null || true
    sleep 2
    if systemctl is-active --quiet apache2; then
        echo -e "${GREEN}✅ Apache démarré${NC}"
    else
        echo -e "${YELLOW}⚠️  Apache n'est pas actif${NC}"
    fi
fi
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
echo "║  📅 Date: $(date '+%d/%m/%Y à %H:%M:%S')"
echo "║                                                                        ║"
echo "║  ✅ Étapes complétées:                                               ║"
echo "║    • Paquets système installés                                        ║"
echo "║    • Repository cloné                                                 ║"
echo "║    • Dépendances Python installées                                    ║"
echo "║    • Permissions configurées                                          ║"
echo "║    • Apache vérifiés                                                  ║"
echo "║                                                                        ║"
echo "║  🎯 PROCHAINES ÉTAPES (à faire manuellement):                        ║"
echo "║                                                                        ║"
echo "║  1️⃣  Configurer Apache:                                              ║"
echo "║     sudo /var/www/SAE203/setup-apache.sh                             ║"
echo "║                                                                        ║"
echo "║  2️⃣  Lancer Django:                                                  ║"
echo "║     sudo /var/www/SAE203/start-django.sh                             ║"
echo "║                                                                        ║"
echo "║  3️⃣  Remplir la base de données (optionnel):                         ║"
echo "║     python3 /var/www/SAE203/populate_db.py                           ║"
echo "║                                                                        ║"
echo "║  4️⃣  Accéder à l'application:                                        ║"
echo "║     http://localhost                                                 ║"
echo "║                                                                        ║"
echo "║  🚀 La VM est prête pour SAE203 !                                     ║"
echo "║                                                                        ║"
echo "╚════════════════════════════════════════════════════════════════════════╝"
echo ""

exit 0
