#!/bin/bash

COWRIE_DIR="/home/cowrie/cowrie"
VENV="$COWRIE_DIR/cowrie-env/bin/activate"
COWRIE_BIN="$COWRIE_DIR/bin/cowrie"
REPORTS_DIR="$COWRIE_DIR"

check_installed() {
    if [ ! -f "$COWRIE_BIN" ]; then
        echo "❌ Cowrie is not installed. Run ./install_cowrie.sh first."
        exit 1
    fi
}

is_running() {
    sudo -u cowrie bash -c "source $VENV && $COWRIE_BIN status" | grep -iq running
}

start_cowrie() {
    sudo -u cowrie bash -c "source $VENV && $COWRIE_BIN start"
}

stop_cowrie() {
    sudo -u cowrie bash -c "source $VENV && $COWRIE_BIN stop"
}

status_cowrie() {
    sudo -u cowrie bash -c "source $VENV && $COWRIE_BIN status"
}

run_reports() {
    if ! is_running; then
        echo "⚠️ Cowrie is not running. Start it first."
        read -p "Press Enter to return..."
        return
    fi

    while true; do
        clear
        echo "=== Cowrie Reports ==="
        echo "1) Top IPs by Event Count"
        echo "2) Number of Attacks Over Time"
        echo "3) Date-wise Event Counts"
        echo "4) Event Type Distribution"
        echo "5) Return to Main Menu"
        read -p "Choice [1-5]: " choice

        case $choice in
            1) sudo -u cowrie bash -c "source $VENV && python $REPORTS_DIR/top_ips.py"; read -p "Press Enter..." ;;
            2) sudo -u cowrie bash -c "source $VENV && python $REPORTS_DIR/attacks_over_time.py"; read -p "Press Enter..." ;;
            3) sudo -u cowrie bash -c "source $VENV && python $REPORTS_DIR/date_wise_events.py"; read -p "Press Enter..." ;;
            4) sudo -u cowrie bash -c "source $VENV && python $REPORTS_DIR/event_type_distribution.py"; read -p "Press Enter..." ;;
            5) break ;;
            *) echo "Invalid choice." ;;
        esac
    done
}

# === MAIN MENU ===

check_installed

while true; do
    clear
    echo "====== Cowrie Manager ======"
    echo "1) Start Cowrie"
    echo "2) Stop Cowrie"
    echo "3) Status"
    echo "4) Run Reports"
    echo "5) Exit"
    read -p "Choose [1-5]: " action

    case $action in
        1) start_cowrie ;;
        2) stop_cowrie ;;
        3) status_cowrie; read -p "Press Enter..." ;;
        4) run_reports ;;
        5) echo "Exiting..."; break ;;
        *) echo "Invalid choice"; sleep 1 ;;
    esac
done
