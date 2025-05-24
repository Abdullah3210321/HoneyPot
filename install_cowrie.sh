#!/bin/bash

echo "=== Step 1: Installing system dependencies ==="
sudo apt update
sudo apt install -y git python3-pip python3-venv libssl-dev libffi-dev build-essential libpython3-dev python3-minimal authbind

echo "=== Step 2: Creating 'cowrie' user if not exists ==="
if id "cowrie" &>/dev/null; then
    echo "User 'cowrie' already exists."
else
    sudo adduser --disabled-password --gecos "" cowrie
    echo "User 'cowrie' created."
fi

echo "=== Step 3: Cloning Cowrie repository into /home/cowrie ==="
sudo -u cowrie bash -c "
    cd /home/cowrie
    if [ ! -d cowrie ]; then
        git clone http://github.com/cowrie/cowrie
    else
        echo 'Cowrie already cloned.'
    fi
"

echo "=== Step 4: Setting up virtual environment ==="
sudo -u cowrie bash -c "
    cd /home/cowrie/cowrie
    python3 -m venv cowrie-env
    source cowrie-env/bin/activate
    pip install --upgrade pip
    pip install --upgrade -r requirements.txt
"

echo "=== Step 5: Enabling telnet support ==="
sudo -u cowrie bash -c "
    cd /home/cowrie/cowrie
    if ! grep -q 'enabled = true' etc/cowrie.cfg.dist; then
        echo '[telnet]' >> etc/cowrie.cfg.dist
        echo 'enabled = true' >> etc/cowrie.cfg.dist
    fi
    if [ ! -f etc/cowrie.cfg ]; then
        cp etc/cowrie.cfg.dist etc/cowrie.cfg
    fi
"

echo "=== Step 6: Setting iptables to redirect port 22 to 2222 ==="
sudo iptables -t nat -A PREROUTING -p tcp --dport 22 -j REDIRECT --to-port 2222

echo "✅ Installation completed successfully."
