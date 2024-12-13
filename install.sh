#!/bin/bash

# Couleurs pour les messages
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Fonction pour afficher les messages
print_message() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Vérifier si le script est exécuté en tant que root
if [ "$EUID" -ne 0 ]; then 
    print_error "Ce script doit être exécuté en tant que root (sudo ./install.sh)"
    exit 1
fi

# Demander les paramètres de configuration
read -p "Entrez le port série du Xcom-232i (par défaut: /dev/ttyUSB0): " SERIAL_PORT
SERIAL_PORT=${SERIAL_PORT:-/dev/ttyUSB0}

read -p "Entrez l'adresse IP du broker MQTT (par défaut: localhost): " MQTT_BROKER
MQTT_BROKER=${MQTT_BROKER:-localhost}

read -p "Entrez le port MQTT (par défaut: 1883): " MQTT_PORT
MQTT_PORT=${MQTT_PORT:-1883}

read -p "Entrez le nom d'utilisateur MQTT (par défaut: ha-mqtt): " MQTT_USER
MQTT_USER=${MQTT_USER:-ha-mqtt}

read -p "Entrez le mot de passe MQTT (par défaut: ha-mqtt): " MQTT_PASSWORD
MQTT_PASSWORD=${MQTT_PASSWORD:-ha-mqtt}

# Installation des dépendances système
print_message "Installation des dépendances système..."
apt-get update
apt-get install -y python3 python3-pip git

# Création du répertoire d'installation
INSTALL_DIR="/opt/xcom-protocol"
print_message "Création du répertoire d'installation dans $INSTALL_DIR"
mkdir -p $INSTALL_DIR
cd $INSTALL_DIR

# Clonage du dépôt
print_message "Clonage du dépôt..."
if [ -d "$INSTALL_DIR/.git" ]; then
    git pull
else
    git clone https://github.com/Jackylaviss/xcom-protocol.git .
fi

# Création du fichier de configuration
print_message "Création du fichier de configuration..."
cat > $INSTALL_DIR/config.py << EOL
# Configuration Xcom
SERIAL_DEVICE = "${SERIAL_PORT}"
BAUDRATE = 115200

# Configuration MQTT
MQTT_BROKER = "${MQTT_BROKER}"
MQTT_PORT = ${MQTT_PORT}
MQTT_CLIENT_ID = "xcom-sensor-client"
MQTT_USERNAME = "${MQTT_USER}"
MQTT_PASSWORD = "${MQTT_PASSWORD}"
EOL

# Installation des dépendances Python
print_message "Installation des dépendances Python..."
pip3 install -r requirements.txt

# Création du service systemd
print_message "Création du service systemd..."
cat > /etc/systemd/system/xcom-protocol.service << EOL
[Unit]
Description=Xcom Protocol Service
After=network.target mosquitto.service
Wants=mosquitto.service

[Service]
Type=simple
User=root
WorkingDirectory=${INSTALL_DIR}
ExecStart=/usr/bin/python3 ${INSTALL_DIR}/Studer.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOL

# Recharger systemd
print_message "Configuration du service..."
systemctl daemon-reload
systemctl enable xcom-protocol
systemctl start xcom-protocol

print_message "Installation terminée !"
echo -e "${GREEN}----------------------------------------${NC}"
echo "Le service est maintenant configuré et démarré."
echo "Commandes utiles :"
echo "  - Voir l'état du service : sudo systemctl status xcom-protocol"
echo "  - Voir les logs : sudo journalctl -u xcom-protocol -f"
echo "  - Redémarrer le service : sudo systemctl restart xcom-protocol"
echo -e "${GREEN}----------------------------------------${NC}"

# Vérification finale
if systemctl is-active --quiet xcom-protocol; then
    print_message "Le service est en cours d'exécution"
else
    print_warning "Le service n'a pas démarré. Vérifiez les logs avec : sudo journalctl -u xcom-protocol -f"
fi
