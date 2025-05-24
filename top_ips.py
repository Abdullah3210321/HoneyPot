import os
import json
import logging
from collections import defaultdict
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
ip_event_counts = defaultdict(int)

logging.info(f"Starting to parse JSON log files in directory: {log_dir}")

try:
    files_found = False

    # Use glob to match both 'cowrie.json' and 'cowrie.json.*'
    log_files = glob.glob(os.path.join(log_dir, "cowrie.json*"))

    if not log_files:
        logging.error(f"No log files found in {log_dir}")
        print("No log files found.")
        exit()

    for filepath in sorted(log_files):
        files_found = True
        logging.info(f"Processing file: {filepath}")
        with open(filepath, "r") as f:
            for line_num, line in enumerate(f, start=1):
                try:
                    log = json.loads(line.strip())
                    ip = log.get("src_ip")
                    if ip:
                        ip_event_counts[ip] += 1
                    else:
                        logging.debug(f"No 'src_ip' at {filepath} line {line_num}")
                except json.JSONDecodeError as e:
                    logging.warning(f"JSON decode error at {filepath} line {line_num}: {e}")

except Exception as e:
    logging.error(f"Exception occurred during log parsing: {e}")
    raise

# Sort and select top IPs
sorted_data = sorted(ip_event_counts.items(), key=lambda x: x[1], reverse=True)
top_n = 10
ips = [ip for ip, _ in sorted_data[:top_n]]
counts = [count for _, count in sorted_data[:top_n]]

if not ips:
    logging.error("No IP data found in JSON log files.")
    print("No IP data found in JSON log files.")
    exit()

logging.info(f"Top {top_n} IPs: {ips}")
logging.info(f"Counts: {counts}")

# Print summary
total_events = sum(ip_event_counts.values())
unique_ips = len(ip_event_counts)
print(f"Total unique IPs: {unique_ips}")
print(f"Total events: {total_events}")
print(f"Showing top {top_n} IPs")

# Plot chart
plt.clear_figure()
plt.title("Top Attacker IPs by Event Count")
plt.bar(ips, counts)
plt.xlabel("IP Address")
plt.ylabel("Event Count")
plt.canvas_color("default")
plt.axes_color("default")
plt.ticks_color("default")
plt.show()
