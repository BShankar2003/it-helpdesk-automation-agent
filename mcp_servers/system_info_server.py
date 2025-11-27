# mcp_servers/system_info_server.py
from flask import Flask, request, jsonify
import random, platform, time

app = Flask(__name__)

@app.route('/system_info', methods=['POST'])
def system_info():
    data = request.json or {}
    device = data.get("device_id", "unknown")
    # simulate system info
    info = {
        "device_id": device,
        "os": platform.system() + " " + platform.release(),
        "cpu_percent": round(random.uniform(5, 95), 1),
        "memory_percent": round(random.uniform(10, 95), 1),
        "disk_percent": round(random.uniform(10, 95), 1),
        "processes_top": [
            {"name":"chrome.exe","memory_mb":random.randint(200,3000)},
            {"name":"python.exe","memory_mb":random.randint(50,800)}
        ],
        "time": time.time()
    }
    return jsonify(info), 200

if __name__ == "__main__":
    app.run(port=8002)
