# mcp_servers/ping_server.py
from flask import Flask, request, jsonify
import random, time

app = Flask(__name__)

@app.route('/ping', methods=['POST'])
def ping():
    data = request.json or {}
    host = data.get("host", "unknown")
    # simulate unreachable host
    if host in ["unreachable", "OFFLINE"]:
        return jsonify({"success": False, "rtt_ms": None, "details": f"Host {host} unreachable"}), 200
    # else simulate good ping
    rtt = round(random.uniform(10, 150), 2)
    time.sleep(0.1)
    return jsonify({"success": True, "rtt_ms": rtt, "details": f"Simulated ping to {host}"}), 200

if __name__ == "__main__":
    app.run(port=8001)
