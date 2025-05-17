#!/bin/bash

source ~/cowrie-tools/bin/activate

while true; do
    clear
    echo "===== Cowrie Logs Report Menu ====="
    echo "1) Top IPs by Event Count"
    echo "2) Number of Attacks Over Time"
    echo "3) Date-wise Event Counts"
    echo "4) Event Type Distribution"
    echo "5) Exit"
    echo
    read -p "Enter your choice [1-5]: " choice

    case $choice in
        1)
            echo "Running Top IPs report..."
            python /home/cowrie/cowrie/top_ips.py
            read -p "Press Enter to return to menu..."
            ;;
        2)
            echo "Running Attacks Over Time report..."
            python /home/cowrie/cowrie/attacks_over_time.py
            read -p "Press Enter to return to menu..."
            ;;
	3)
            echo "Running Date-wise Event Counts report..."
            python /home/cowrie/cowrie/date_wise_events.py
            read -p "Press Enter to return to menu..."
            ;;
        4)
            echo "Running Event Type Distribution report..."
            python /home/cowrie/cowrie/event_type_distribution.py
            read -p "Press Enter to return to menu..."
            ;;
         5)
            echo "Exiting..."
            break
            ;;
        *)
            echo "Invalid choice, please try again."
            sleep 1
            ;;
    esac
done

