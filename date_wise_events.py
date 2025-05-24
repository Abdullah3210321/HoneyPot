import os
import json
import logging
from collections import defaultdict
from datetime import datetime
import plotext as plt
import glob

# Setup logging
logging.basicConfig(
    filename='cowrie_log_debug.log',
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

log_dir = "/home/cowrie/cowrie/var/log/cowrie"
date_event_counts = defaultdict(int)

logging.info(f"Starting to parse JSON log files in directory: {log_dir}")

try:
    # Use glob to match both 'cowrie.json' and 'cowrie.json.*'
    log_files = glob.glob(os.path.join(log_dir, "cowrie.json*"))

    if not log_files:
        logging.error("No log files found.")
        print("No Cowrie log files found.")
        exit()

    for filepath in sorted(log_files):
        logging.info(f"Processing file: {filepath}")

        with open(filepath, "r") as f:
            for line_num, line in enumerate(f, 1):
                try:
                    log_entry = json.loads(line.strip())
                    timestamp = log_entry.get("timestamp")

                    if timestamp:
                        try:
                            date_str = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ").date().isoformat()
                            date_event_counts[date_str] += 1
                        except ValueError:
                            logging.debug(f"Invalid timestamp format at {filepath} line {line_num}: {timestamp}")
                    else:
                        logging.debug(f"No 'timestamp' found at {filepath} line {line_num}")
                except json.JSONDecodeError as e:
                    logging.warning(f"JSON decode error at {filepath} line {line_num}: {e}")

except Exception as e:
    logging.error(f"Exception occurred during log parsing: {e}")
    raise

if not date_event_counts:
    logging.error("No valid date event data found.")
    print("No date-wise event data found.")
    exit()

# Sort by date
sorted_dates = sorted(date_event_counts.items())
dates = [d for d, _ in sorted_dates]
counts = [c for _, c in sorted_dates]

total_events = sum(counts)

print("Running Date-wise Event Counts report...")
print(f"Total events: {total_events}")
print(f"Total active days: {len(dates)}")
print("Showing date-wise event distribution")

# Plotting using index-based x-axis to avoid date parsing issues
x_indices = list(range(len(dates)))
labels_to_show = dates

plt.clear_figure()
plt.title("Date-wise Event Counts")
plt.bar(x_indices, counts)
plt.xlabel("Date Index")
plt.ylabel("Event Count")
plt.xticks(x_indices[::max(1, len(x_indices)//10)], labels_to_show[::max(1, len(labels_to_show)//10)])  # limit clutter
plt.show()
