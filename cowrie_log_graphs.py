import json
import time
import logging
from collections import Counter
import plotext as plt
import os

# Configure logging
logging.basicConfig(
    filename='cowrie_plot_debug.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

log_path = '/home/cowrie/cowrie/var/log/cowrie/cowrie.json'

def load_initial_data():
    """Load all existing logs and count event types."""
    event_counter = Counter()
    try:
        with open(log_path, 'r') as f:
            for line in f:
                try:
                    data = json.loads(line)
                    eventid = data.get("eventid")
                    if eventid:
                        event_counter[eventid] += 1
                except json.JSONDecodeError as e:
                    logging.warning(f"Bad JSON: {e}")
    except FileNotFoundError:
        logging.error(f"Log file not found: {log_path}")
    return event_counter

def tail_log():
    """Yield new log lines as they come in."""
    try:
        with open(log_path, 'r') as f:
            f.seek(0, os.SEEK_END)
            while True:
                line = f.readline()
                if not line:
                    time.sleep(1)
                    continue
                yield line
    except Exception as e:
        logging.error(f"Error in tail_log: {e}")

def plot_event_graph(counter):
    """Plot current event counts using plotext."""
    try:
        plt.clear_data()  # FIXED: correct way to clear previous plot data
        if not counter:
            plt.plotsize(100, 20)
            plt.title("No events found.")
            plt.show()
            return

        events, counts = zip(*counter.most_common(10))
        plt.bar(events, counts, orientation='horizontal', color='cyan')
        plt.title("Cowrie Event Counts (Live)")
        plt.xlabel("Count")
        plt.ylabel("Event Type")
        plt.plotsize(100, 25)
        plt.show()
    except Exception as e:
        logging.error(f"Error plotting: {e}")

def main():
    logging.info("Script started. Loading initial data...")
    event_counter = load_initial_data()
    plot_event_graph(event_counter)
    logging.info("Starting live monitoring...")

    for line in tail_log():
        try:
            data = json.loads(line)
            eventid = data.get("eventid")
            if eventid:
                event_counter[eventid] += 1
                plot_event_graph(event_counter)
        except json.JSONDecodeError as e:
            logging.warning(f"Skipping invalid JSON: {e}")
        except Exception as e:
            logging.error(f"Unexpected error in live monitoring: {e}")

if __name__ == "__main__":
    main()
