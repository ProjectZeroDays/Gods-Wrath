#!/bin/bash

# Create configuration directory
CONFIG_DIR="$HOME/.config/audit_tool"
mkdir -p "$CONFIG_DIR"

# Generate encryption key
SECRET_KEY_PATH="$CONFIG_DIR/secret.key"
if [ ! -f "$SECRET_KEY_PATH" ]; then
    python3 -c "from cryptography.fernet import Fernet; key = Fernet.generate_key(); open('$SECRET_KEY_PATH', 'wb').write(key)"
    echo "Encryption key generated and saved to $SECRET_KEY_PATH"
else
    echo "Encryption key already exists at $SECRET_KEY_PATH"
fi

# Install required Python packages
pip install -r requirements.txt

# Install Sn1per
git clone https://github.com/1N3/Sn1per.git
cd Sn1per
sudo bash install.sh
cd ..

echo "Installation complete."
