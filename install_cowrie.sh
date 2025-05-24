#!/bin/bash

# === Variables ===
COWRIE_USER="cowrie"
COWRIE_HOME="/home/$COWRIE_USER"
GIT_REPO="https://github.com/cowrie/cowrie"
COWRIE_DIR="$COWRIE_HOME/cowrie"
TOOLS_SOURCE_DIR="$(pwd)/tools"        # Assuming your Python scripts & cowrie_manager.sh are here
TOOLS_TARGET_DIR="$COWRIE_DIR/tools"

# === Functions ===

check_installed() {
    if id "$COWRIE_USER" &>/dev/null && [ -d "$COWRIE_DIR" ]; then
        echo "[✔] Cowrie is already installed."
        return 0
    else
        return 1
    fi
}

install_dependencies() {
    echo "[ℹ] Installing system dependencies..."
    sudo apt-get update
    sudo apt-get install -y git python3-pip python3-venv libssl-dev libffi-dev build-essential libpython3-dev python3-minimal authbind
}

create_user() {
    echo "[ℹ] Creating user 'cowrie'..."
    sudo adduser --disabled-password --gecos "" $COWRIE_USER
}

clone_repo() {
    echo "[ℹ] Cloning Cowrie from GitHub..."
    sudo -u $COWRIE_USER git clone $GIT_REPO $COWRIE_DIR
}

setup_virtualenv() {
    echo "[ℹ] Setting up Python virtual environment..."
    sudo -u $COWRIE_USER bash -c "
        cd $COWRIE_DIR &&
        python3 -m venv cowrie-env &&
        source cowrie-env/bin/activate &&
        pip install --upgrade pip &&
        pip install --upgrade -r requirements.txt
    "
}

configure_telnet() {
    echo "[ℹ] Enabling Telnet in configuration..."
    CONFIG_FILE="$COWRIE_DIR/etc/cowrie.cfg"
    if ! grep -q "\[telnet\]" "$CONFIG_FILE"; then
        echo -e "\n[telnet]\nenabled = true" | sudo tee -a "$CONFIG_FILE" > /dev/null
    fi
}

setup_iptables() {
    echo "[ℹ] Redirecting port 22 to Cowrie (2222)..."
    sudo iptables -t nat -A PREROUTING -p tcp --dport 22 -j REDIRECT --to-port 2222
}

move_management_scripts() {
    echo "[ℹ] Moving management scripts to Cowrie directory..."
    sudo mkdir -p "$TOOLS_TARGET_DIR"
    sudo cp -r "$TOOLS_SOURCE_DIR/"* "$TOOLS_TARGET_DIR/"
    sudo chown -R $COWRIE_USER:$COWRIE_USER "$TOOLS_TARGET_DIR"
}

add_logrotate_cron() {
    echo "[ℹ] Adding log rotation cron job..."
    LOG_CLEAN_SCRIPT="$COWRIE_DIR/tools/rotate_logs.sh"
    sudo -u $COWRIE_USER bash -c "cat > $LOG_CLEAN_SCRIPT" << 'EOF'
#!/bin/bash
find /home/cowrie/cowrie/var/log/cowrie/ -name "*.log*" -mtime +7 -exec rm -f {} \;
EOF
    chmod +x "$LOG_CLEAN_SCRIPT"
    (sudo crontab -u $COWRIE_USER -l 2>/dev/null; echo "0 2 * * * $LOG_CLEAN_SCRIPT") | sudo crontab -u $COWRIE_USER -
}

# === Execution Starts Here ===

echo "========== Cowrie Auto Installer =========="

if check_installed; then
    echo "[ℹ] Skipping installation steps."
else
    install_dependencies
    create_user
    clone_repo
    setup_virtualenv
    configure_telnet
    setup_iptables
    move_management_scripts
    add_logrotate_cron
fi

echo
echo "[✅] Cowrie setup is complete!"
echo "[ℹ] Cowrie management script: $TOOLS_TARGET_DIR/cowrie_manager.sh"

read -p "Do you want to run the Cowrie Manager now? [Y/n]: " launch_choice
launch_choice=${launch_choice:-Y}

if [[ "$launch_choice" =~ ^[Yy]$ ]]; then
    echo "[🚀] Launching Cowrie Manager as user 'cowrie'..."
    sudo -u cowrie bash "$TOOLS_TARGET_DIR/cowrie_manager.sh"
else
    echo "[ℹ] You can run it later using:"
    echo "    sudo -u cowrie bash $TOOLS_TARGET_DIR/cowrie_manager.sh"
fi
