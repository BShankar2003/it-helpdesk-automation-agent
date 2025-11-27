# agents/run_demo.py
import os, sys

# Ensure project root is on sys.path so package imports resolve correctly
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# now normal imports
import json, time, os
from agents.coordinator import process_ticket


DATA_PATH = "data/tickets.json"

def load_tickets():
    with open(DATA_PATH,"r") as f:
        return json.load(f)

def run():
    tickets = load_tickets()
    results = []
    for t in tickets:
        print(f"[demo] processing {t['ticket_id']} - {t['issue']}")
        res = process_ticket(t)
        results.append(res)
        time.sleep(0.2)
    # save aggregated results
    os.makedirs("outputs", exist_ok=True)
    with open("outputs/results.json","w") as f:
        json.dump(results, f, indent=2)
    print("[demo] done. results saved to outputs/results.json")

if __name__ == "__main__":
    run()
