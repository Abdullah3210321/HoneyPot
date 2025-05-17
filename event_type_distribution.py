import os
import json
import logging
from collections import defaultdict
import plotext as plt

# Setup logging
logging.basicConfig(
    filename='event_type_debug.log',
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

log_dir = "/home/cowrie/cowrie/var/log/cowrie"
event_type_counts = defaultdict(int)

# Only these meaningful events will be counted and plotted
important_events = {
    "cowrie.login.failed",
    "cowrie.login.success",
    "cowrie.command.input",
    "cowrie.session.file_download",
    "cowrie.session.file_upload",
    "cowrie.client.version",
    "cowrie.session.connect",
    "cowrie.session.closed"
}

logging.info(f"Starting to parse JSON log files in directory: {log_dir}")

try:
    files_found = False
    for file in os.listdir(log_dir):
        if file.startswith("cowrie.json."):
            files_found = True
            filepath = os.path.join(log_dir, file)
            logging.info(f"Processing file: {filepath}")

            with open(filepath, "r") as f:
                for line_num, line in enumerate(f, 1):
                    try:
                        log_entry = json.loads(line.strip())
                        event_type = log_entry.get("eventid")

                        if event_type in important_events:
                            event_type_counts[event_type] += 1
                    except json.JSONDecodeError as e:
                        logging.warning(f"JSON decode error at {filepath} line {line_num}: {e}")
    
    if not files_found:
        logging.error("No log files starting with 'cowrie.json.' found.")
        print("No Cowrie log files found.")
        exit()

except Exception as e:
    logging.error(f"Exception occurred during log parsing: {e}")
    raise

if not event_type_counts:
    logging.error("No valid event type data found.")
    print("No relevant event types found.")
    exit()

# Sort by count descending
sorted_event_types = sorted(event_type_counts.items(), key=lambda x: x[1], reverse=True)
event_names = [etype for etype, _ in sorted_event_types]
event_counts = [count for _, count in sorted_event_types]

total_events = sum(event_counts)

print("Running Event Type Distribution report...")
print(f"Total filtered events: {total_events}")
print(f"Total event types shown: {len(event_names)}")
print("Showing event type distribution:")

# Plot
plt.clear_figure()
plt.title("Key Event Type Distribution")
plt.bar(event_names, event_counts)
plt.xlabel("Event Type")
plt.ylabel("Count")
plt.show()
