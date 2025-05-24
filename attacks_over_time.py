import os
import json
import logging
from collections import defaultdict
from datetime import datetime
import plotext as plt
import glob

# Setup logging
logging.basicConfig(
    filename='attacks_over_time_debug.log',
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

log_dir = "/home/cowrie/cowrie/var/log/cowrie"
date_attack_counts = defaultdict(int)

# Define event types considered "attacks"
attack_events = {
    "cowrie.login.failed",
    "cowrie.command.input",
    "cowrie.session.file_download",
    "cowrie.session.file_upload"
}

logging.info(f"Starting to parse JSON log files in directory: {log_dir}")

try:
    files_found = False

    # Use glob to match both 'cowrie.json' and 'cowrie.json.*'
    log_files = glob.glob(os.path.join(log_dir, "cowrie.json*"))

    if not log_files:
        logging.error("No log files found.")
        print("No Cowrie log files found.")
        exit()

    for filepath in sorted(log_files):
        files_found = True
        logging.info(f"Processing file: {filepath}")

        with open(filepath, "r") as f:
            for line_num, line in enumerate(f, 1):
                try:
                    log_entry = json.loads(line.strip())
                    timestamp = log_entry.get("timestamp")
                    event_type = log_entry.get("eventid")

                    if timestamp and event_type in attack_events:
                        try:
                            date_str = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ").date().isoformat()
                            date_attack_counts[date_str] += 1
                        except ValueError:
                            logging.debug(f"Invalid timestamp format at {filepath} line {line_num}: {timestamp}")
                except json.JSONDecodeError as e:
                    logging.warning(f"JSON decode error at {filepath} line {line_num}: {e}")

except Exception as e:
    logging.error(f"Exception occurred during log parsing: {e}")
    raise

if not date_attack_counts:
    logging.error("No attack-related events found.")
    print("No attack events found.")
    exit()

# Sort by date
sorted_dates = sorted(date_attack_counts.items())
dates = [d for d, _ in sorted_dates]
counts = [c for _, c in sorted_dates]

total_attacks = sum(counts)

print("Running Number of Attacks Over Time report...")
print(f"Total attack events: {total_attacks}")
print(f"Total days recorded: {len(dates)}")
print("Showing attack trend over time:")

# Plotting
x_indices = list(range(len(dates)))

plt.clear_figure()
plt.title("Number of Attacks Over Time")
plt.plot(x_indices, counts, marker="dot")
plt.xlabel("Date Index")
plt.ylabel("Number of Attacks")
plt.xticks(x_indices[::max(1, len(x_indices)//10)], dates[::max(1, len(dates)//10)])  # limit label clutter
plt.show()

