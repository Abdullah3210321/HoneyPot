import os
import json
import logging
from collections import defaultdict
import plotext as plt

# Setup logging
logging.basicConfig(
    filename='cowrie_log_debug.log',  # Log file path
    level=logging.DEBUG,               # Capture all levels of logs (DEBUG and above)
    format='%(asctime)s %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

log_dir = "/home/cowrie/cowrie/var/log/cowrie"
ip_event_counts = defaultdict(int)

logging.info(f"Starting to parse JSON log files in directory: {log_dir}")

try:
    files_found = False
    # Loop through all JSON log files (cowrie.json.*)
    for file in os.listdir(log_dir):
        if file.startswith("cowrie.json."):
            files_found = True
            filepath = os.path.join(log_dir, file)
            logging.info(f"Processing file: {filepath}")

            with open(filepath, "r") as f:
                line_num = 0
                for line in f:
                    line_num += 1
                    try:
                        log = json.loads(line.strip())
                        ip = log.get("src_ip")
                        if ip:
                            ip_event_counts[ip] += 1
                        else:
                            logging.debug(f"No 'src_ip' found at {filepath} line {line_num}")
                    except json.JSONDecodeError as e:
                        logging.warning(f"JSON decode error at {filepath} line {line_num}: {e}")

    if not files_found:
        logging.error(f"No files starting with 'cowrie.json.' found in {log_dir}")

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

# Print summary info
total_events = sum(ip_event_counts.values())
unique_ips = len(ip_event_counts)
print(f"Total unique IPs: {unique_ips}")
print(f"Total events: {total_events}")
print(f"Showing top {top_n} IPs + Others grouped")

# Plot bar chart
plt.clear_figure()
plt.title("Top Attacker IPs by Event Count")
plt.bar(ips, counts)
plt.xlabel("IP Address")
plt.ylabel("Event Count")
plt.show()
