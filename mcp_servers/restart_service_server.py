# mcp_servers/restart_service_server.py
from flask import Flask, request, jsonify
import time

app = Flask(__name__)

@app.route('/restart_service', methods=['POST'])
def restart_service():
    data = request.json or {}
    device = data.get("device_id", "")
    service = data.get("service_name", "unknown")
    # PoC policy:
    # - If device looks like production (starts with 'PROD'), require manual approval.
    # - Else simulate success.
    requires_approval = False
    if str(device).upper().startswith("PROD"):
        requires_approval = True
    # Also simulate that restarts always succeed when not requiring approval
    if requires_approval:
        response = {
            "requires_approval": True,
            "message": f"Restart of {service} on {device} is blocked by policy - requires manual approval."
        }
    else:
        # simulate restart delay
        time.sleep(0.2)
        response = {
            "requires_approval": False,
            "status": "restarted",
            "message": f"Service {service} on {device} restarted successfully (simulated)."
        }
    return jsonify(response), 200

if __name__ == "__main__":
    app.run(port=8004)
