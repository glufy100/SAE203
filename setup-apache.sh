#!/bin/bash

# ═══════════════════════════════════════════════════════════════════════════
# Script de configuration Apache pour SAE203
# Configure le VirtualHost et les modules nécessaires
# ═══════════════════════════════════════════════════════════════════════════

set +e

echo "╔════════════════════════════════════════════════════════════════════════╗"
echo "║        ⚙️  CONFIGURATION APACHE POUR SAE203                           ║"
echo "╚════════════════════════════════════════════════════════════════════════╝"
echo ""

# Configuration
PROJECT_PATH="/var/www/SAE203"
APACHE_CONFIG="/etc/apache2/sites-available/sae203.conf"

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
# Étape 1: Vérifier que le projet existe
# ═══════════════════════════════════════════════════════════════════════════

echo -e "${BLUE}📂 Étape 1: Vérification du répertoire du projet...${NC}"
if [ ! -d "$PROJECT_PATH" ]; then
    echo -e "${RED}❌ Le répertoire $PROJECT_PATH n'existe pas${NC}"
    echo -e "${YELLOW}   Exécutez d'abord: sudo ./init-vm.sh${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Répertoire trouvé: $PROJECT_PATH${NC}"
echo ""

# ═══════════════════════════════════════════════════════════════════════════
# Étape 2: Activer les modules Apache nécessaires
# ═══════════════════════════════════════════════════════════════════════════

echo -e "${BLUE}⚙️  Étape 2: Activation des modules Apache...${NC}"

# Modules essentiels pour Django - proxy_http est le minimum requis
MODULES=("proxy" "proxy_http")

for module in "${MODULES[@]}"; do
    if a2enmod "$module" 2>&1 | grep -q "enabled\|already"; then
        echo -e "   ${GREEN}✅ Module $module activé${NC}"
    else
        echo -e "   ${RED}❌ Erreur pour le module $module${NC}"
    fi
done

# Modules optionnels
OPTIONAL_MODULES=("rewrite" "headers" "wsgi")
for module in "${OPTIONAL_MODULES[@]}"; do
    if a2enmod "$module" 2>&1 | grep -q "enabled\|already"; then
        echo -e "   ${GREEN}✅ Module $module activé (optionnel)${NC}"
    else
        echo -e "   ${YELLOW}⚠️  Module $module non disponible (optionnel)${NC}"
    fi
done
echo ""

# ═══════════════════════════════════════════════════════════════════════════
# Étape 3: Créer la configuration VirtualHost
# ═══════════════════════════════════════════════════════════════════════════

echo -e "${BLUE}📝 Étape 3: Création de la configuration VirtualHost...${NC}"

cat > "$APACHE_CONFIG" << 'EOF'
<VirtualHost *:80>
    ServerName sae203.local
    ServerAlias localhost
    DocumentRoot /var/www/SAE203

    # Logs
    ErrorLog ${APACHE_LOG_DIR}/sae203_error.log
    CustomLog ${APACHE_LOG_DIR}/sae203_access.log combined

    # Activer le proxy
    <IfModule mod_proxy.c>
        ProxyPreserveHost On

        # Rediriger tout vers Django
        ProxyPass / http://127.0.0.1:8000/
        ProxyPassReverse / http://127.0.0.1:8000/
    </IfModule>

    # Root directory
    <Directory /var/www/SAE203>
        Require all granted
    </Directory>

    # Deny access to sensitive files
    <FilesMatch "^\.">
        Require all denied
    </FilesMatch>

    <FilesMatch "\.py$">
        Require all denied
    </FilesMatch>

</VirtualHost>
EOF

if [ -f "$APACHE_CONFIG" ]; then
    echo -e "${GREEN}✅ Configuration VirtualHost créée${NC}"
    echo -e "   Chemin: $APACHE_CONFIG"
else
    echo -e "${RED}❌ Erreur lors de la création de la configuration${NC}"
    exit 1
fi
echo ""

# ═══════════════════════════════════════════════════════════════════════════
# Étape 4: Désactiver le site par défaut et activer SAE203
# ═══════════════════════════════════════════════════════════════════════════

echo -e "${BLUE}🔧 Étape 4: Activation du site SAE203...${NC}"

# Désactiver le site par défaut
if a2dissite 000-default 2>&1 | grep -q "Site\|disabled"; then
    echo -e "   ${GREEN}✅ Site par défaut désactivé${NC}"
fi

# Activer le site SAE203
SITE_OUTPUT=$(a2ensite sae203 2>&1)
if echo "$SITE_OUTPUT" | grep -q "enabled\|already"; then
    echo -e "   ${GREEN}✅ Site SAE203 activé${NC}"
else
    echo -e "   ${YELLOW}⚠️  Vérification de l'activation du site${NC}"
    echo "$SITE_OUTPUT"
fi
echo ""

# ═══════════════════════════════════════════════════════════════════════════
# Étape 5: Tester la configuration
# ═══════════════════════════════════════════════════════════════════════════

echo -e "${BLUE}🧪 Étape 5: Test de la configuration Apache...${NC}"
if apache2ctl configtest 2>&1 | grep -q "Syntax OK"; then
    echo -e "${GREEN}✅ Configuration Apache valide${NC}"
else
    echo -e "${YELLOW}⚠️  Problème de configuration détecté${NC}"
    apache2ctl configtest
fi
echo ""

# ═══════════════════════════════════════════════════════════════════════════
# Étape 6: Redémarrer Apache
# ═══════════════════════════════════════════════════════════════════════════

echo -e "${BLUE}🔄 Étape 6: Redémarrage d'Apache...${NC}"
if systemctl reload apache2 2>&1; then
    echo -e "${GREEN}✅ Apache rechargé${NC}"
    sleep 2
    
    if systemctl is-active --quiet apache2; then
        echo -e "${GREEN}✅ Apache fonctionne correctement${NC}"
    else
        echo -e "${RED}❌ Apache ne fonctionne pas${NC}"
        systemctl status apache2
        exit 1
    fi
else
    echo -e "${RED}❌ Erreur lors du rechargement d'Apache${NC}"
    exit 1
fi
echo ""

# ═══════════════════════════════════════════════════════════════════════════
# Résumé final
# ═══════════════════════════════════════════════════════════════════════════

echo "╔════════════════════════════════════════════════════════════════════════╗"
echo "║             ✅ CONFIGURATION APACHE RÉUSSIE !                         ║"
echo "╠════════════════════════════════════════════════════════════════════════╣"
echo "║                                                                        ║"
echo "║  🌐 Apache: ✅ En cours d'exécution                                    ║"
echo "║  📁 Projet: $PROJECT_PATH"
echo "║  ⚙️  Configuration: $APACHE_CONFIG"
echo "║  📅 Heure: $(date '+%d/%m/%Y à %H:%M:%S')"
echo "║                                                                        ║"
echo "║  🎯 Prochaines étapes:                                               ║"
echo "║                                                                        ║"
echo "║  1. Démarrer Django en arrière-plan:                                 ║"
echo "║     cd $PROJECT_PATH                                                 ║"
echo "║     python manage.py runserver 127.0.0.1:8000 &                      ║"
echo "║                                                                        ║"
echo "║  2. Accéder à l'application:                                         ║"
echo "║     http://localhost                                                 ║"
echo "║     ou                                                               ║"
echo "║     http://sae203.local                                              ║"
echo "║                                                                        ║"
echo "║  3. (Optional) Configurer un process manager (Gunicorn/Systemd):    ║"
echo "║     Pour un vrai environnement de production                         ║"
echo "║                                                                        ║"
echo "╚════════════════════════════════════════════════════════════════════════╝"
echo ""

exit 0
