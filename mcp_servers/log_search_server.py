# mcp_servers/log_search_server.py
from flask import Flask, request, jsonify
import os, time

app = Flask(__name__)

LOG_DIR = "data/logs"

@app.route('/search', methods=['POST'])
def search_logs():
    data = request.json or {}
    device = data.get("device_id", "")
    query = (data.get("query","") or "").lower()
    results = []
    # search all logs (simple simulation)
    if not os.path.isdir(LOG_DIR):
        return jsonify({"results":[], "note": "no logs available"}), 200
    for fname in os.listdir(LOG_DIR):
        path = os.path.join(LOG_DIR, fname)
        try:
            with open(path,"r", errors="ignore") as f:
                for line in f:
                    if query and query in line.lower():
                        results.append({"file": fname, "line": line.strip()})
                    # also include some lines when query empty
                    elif not query and "error" in line.lower():
                        results.append({"file": fname, "line": line.strip()})
        except Exception:
            continue
    time.sleep(0.05)
    return jsonify({"results": results[:50]}), 200

if __name__ == "__main__":
    app.run(port=8003)
