#!/bin/bash

# ═══════════════════════════════════════════════════════════════════════════
# Script de déploiement pour SAE203 sur VM Debian
# Mise à jour du code et redémarrage d'Apache
# ═══════════════════════════════════════════════════════════════════════════

# Ne pas arrêter sur erreur pour plus de flexibilité
set +e

echo "╔════════════════════════════════════════════════════════════════════════╗"
echo "║           🚀 DÉPLOIEMENT SAE203 - VM DEBIAN                           ║"
echo "╚════════════════════════════════════════════════════════════════════════╝"
echo ""

# Configuration
PROJECT_PATH="/var/www/SAE203"
REPO_URL="https://github.com/glufy100/SAE203.git"

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Vérifier que le script s'exécute en tant que root
if [ "$EUID" -ne 0 ]; then 
    echo -e "${RED}❌ Ce script doit être exécuté avec sudo${NC}"
    exit 1
fi

echo "📍 Chemin du projet: $PROJECT_PATH"
echo ""

# ═══════════════════════════════════════════════════════════════════════════
# Étape 1: Configurer Git (safe.directory)
# ═══════════════════════════════════════════════════════════════════════════

echo "📦 Étape 1: Configuration de Git..."
git config --global --add safe.directory "$PROJECT_PATH" 2>/dev/null || true
git config --global --add safe.directory "$PROJECT_PATH" --global 2>/dev/null || true
echo -e "${GREEN}✅ Git configuré${NC}"
echo ""

# ═══════════════════════════════════════════════════════════════════════════
# Étape 2: Accéder au répertoire du projet
# ═══════════════════════════════════════════════════════════════════════════

echo "📂 Étape 2: Accès au répertoire du projet..."
if ! cd "$PROJECT_PATH"; then
    echo -e "${RED}❌ Impossible d'accéder à $PROJECT_PATH${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Répertoire: $(pwd)${NC}"
echo ""

# ═══════════════════════════════════════════════════════════════════════════
# Étape 3: Récupérer les dernières modifications
# ═══════════════════════════════════════════════════════════════════════════

echo "🔄 Étape 3: Mise à jour du code..."
echo "   → Récupération des dernières modifications..."
git fetch origin main 2>/dev/null || true
echo "   → Application des changements..."
git reset --hard origin/main 2>/dev/null || git pull origin main 2>/dev/null || true
echo "✅ Code à jour"
echo ""

# ═══════════════════════════════════════════════════════════════════════════
# Étape 4: Vérifier les fichiers principaux
# ═══════════════════════════════════════════════════════════════════════════

echo "🔍 Étape 4: Vérification des fichiers..."
files=("manage.py" "populate_db.py" "requirements.txt" "project/settings.py")
all_files_ok=true
for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo -e "   ${GREEN}✅ $file${NC}"
    else
        echo -e "   ${RED}❌ $file (MANQUANT)${NC}"
        all_files_ok=false
    fi
done
echo ""

if [ "$all_files_ok" = false ]; then
    echo -e "${YELLOW}⚠️ Attention: Certains fichiers sont manquants${NC}"
fi
echo ""

# ═══════════════════════════════════════════════════════════════════════════
# Étape 5: Redémarrer Apache
# ═══════════════════════════════════════════════════════════════════════════

echo "🔄 Étape 5: Redémarrage d'Apache..."
if ! systemctl restart apache2; then
    echo -e "${RED}❌ Erreur lors du redémarrage d'Apache${NC}"
    echo "   Tentative de diagnostic..."
    systemctl status apache2
    exit 1
fi

sleep 2

if systemctl is-active --quiet apache2; then
    echo -e "${GREEN}✅ Apache redémarré avec succès${NC}"
else
    echo -e "${RED}❌ Apache n'est pas actif après redémarrage${NC}"
    systemctl status apache2
    exit 1
fi
echo ""

# ═══════════════════════════════════════════════════════════════════════════
# Résumé final
# ═══════════════════════════════════════════════════════════════════════════

# ═══════════════════════════════════════════════════════════════════════════
# Résumé final
# ═══════════════════════════════════════════════════════════════════════════

echo "╔════════════════════════════════════════════════════════════════════════╗"
echo "║                  ✅ DÉPLOIEMENT RÉUSSI !                             ║"
echo "╠════════════════════════════════════════════════════════════════════════╣"
echo "║                                                                        ║"
echo "║  📁 Projet: $PROJECT_PATH"
echo "║  🔗 Repository: $REPO_URL"
echo "║  🌐 Apache: ✅ En cours d'exécution"
echo "║  📅 Déploiement: $(date '+%d/%m/%Y à %H:%M:%S')"
echo "║                                                                        ║"
echo "║  Votre application SAE203 est maintenant à jour et en ligne ! 🚀      ║"
echo "║                                                                        ║"
echo "╚════════════════════════════════════════════════════════════════════════╝"
echo ""
echo -e "${GREEN}Déploiement terminé avec succès !${NC}"

exit 0
