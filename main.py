# main.py
"""
Simple convenience driver:
- Starts processing all tickets (calls agents/run_demo.py logic)
Run this after starting mock servers.
"""
from agents.run_demo import run

if __name__ == "__main__":
    run()
