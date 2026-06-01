#!/bin/bash

# ═══════════════════════════════════════════════════════════════════════════
# SCRIPT DE VÉRIFICATION PRÉ-DÉPLOIEMENT SAE203
# À exécuter AVANT de lancer init-vm.sh
# ═══════════════════════════════════════════════════════════════════════════

echo "╔════════════════════════════════════════════════════════════════════════╗"
echo "║    🔍 VÉRIFICATION PRÉ-DÉPLOIEMENT SAE203                            ║"
echo "╚════════════════════════════════════════════════════════════════════════╝"
echo ""

# Couleurs
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

ERRORS=0

# Test 1: Connexion Internet
echo "📡 Test 1: Connexion Internet..."
if ping -c 1 github.com > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Connexion OK${NC}"
else
    echo -e "${RED}❌ Pas de connexion à github.com${NC}"
    ERRORS=$((ERRORS + 1))
fi
echo ""

# Test 2: sudo disponible
echo "🔐 Test 2: Commande sudo..."
if sudo -n true 2>/dev/null; then
    echo -e "${GREEN}✅ sudo disponible sans mot de passe${NC}"
else
    echo -e "${RED}⚠️  sudo peut demander un mot de passe${NC}"
fi
echo ""

# Test 3: Espace disque
echo "💾 Test 3: Espace disque..."
SPACE=$(df /var/www 2>/dev/null | awk 'NR==2 {print $4}')
if [ "$SPACE" -gt 5242880 ]; then
    echo -e "${GREEN}✅ Au moins 5GB disponible${NC}"
else
    echo -e "${RED}❌ Moins de 5GB disponible${NC}"
    ERRORS=$((ERRORS + 1))
fi
echo ""

# Test 4: Paquets critiques
echo "📦 Test 4: Paquets système..."
if command -v apt-get > /dev/null 2>&1; then
    echo -e "${GREEN}✅ apt-get disponible${NC}"
else
    echo -e "${RED}❌ apt-get introuvable (Debian required)${NC}"
    ERRORS=$((ERRORS + 1))
fi
echo ""

# Test 5: Répertoire /var/www
echo "📁 Test 5: Répertoire /var/www..."
if [ -d "/var/www" ]; then
    if [ -w "/var/www" ] || sudo -n test -w /var/www 2>/dev/null; then
        echo -e "${GREEN}✅ /var/www accessible${NC}"
    else
        echo -e "${RED}❌ /var/www non accessible${NC}"
        ERRORS=$((ERRORS + 1))
    fi
else
    echo -e "${RED}❌ /var/www n'existe pas${NC}"
    ERRORS=$((ERRORS + 1))
fi
echo ""

# Résumé
echo "╔════════════════════════════════════════════════════════════════════════╗"
if [ $ERRORS -eq 0 ]; then
    echo "║               ✅ TOUS LES TESTS RÉUSSIS !                         ║"
    echo "║                                                                    ║"
    echo "║  Vous pouvez maintenant lancer:                                   ║"
    echo "║  sudo bash -c 'wget -qO- https://raw.githubusercontent.com/glufy100/SAE203/main/init-vm.sh | bash'  ║"
else
    echo "║               ⚠️  $ERRORS TEST(S) ÉCHOUÉ(S)                           ║"
    echo "║                                                                    ║"
    echo "║  Corrigez les problèmes avant de continuer                        ║"
fi
echo "╚════════════════════════════════════════════════════════════════════════╝"
echo ""

exit $ERRORS
