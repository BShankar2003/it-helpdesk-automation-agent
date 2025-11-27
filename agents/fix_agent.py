# agents/fix_agent.py
import requests, json, time, os

MCP_RESTART = "http://127.0.0.1:8004/restart_service"

def attempt_fix(ticket, diagnostics):
    """
    Decide if a fix can be attempted automatically.
    For restart_service (destructive), we require manual approval in PoC.
    """
    device = ticket.get("device_id", "unknown")
    result = {"actions": [], "status": "no_action", "notes": ""}

    # If logs indicate service stopped or ping failed, propose restart
    ping = diagnostics.get("ping", {})
    log = diagnostics.get("log_search", {})
    system = diagnostics.get("system_info", {})

    needs_restart = False
    if ping and isinstance(ping, dict) and not ping.get("success", True):
        needs_restart = True
    if log and isinstance(log, dict):
        # simple heuristic: look for 'service stopped' or 'authentication timeout'
        joined = json.dumps(log).lower()
        if "service stopped" in joined or "authentication" in joined:
            needs_restart = True

    if needs_restart:
        # Attempt non-destructive actions first: recommend steps
        result["actions"].append({"action":"recommendation","details":"Please try restarting the service or network adapter. If allowed, agent can request restart."})
        # Simulate attempting restart but require manual approval
        # We call restart service; the mock server will indicate if approval required
        try:
            resp = requests.post(MCP_RESTART, json={"device_id": device, "service_name": "vpn"}, timeout=5)
            respj = resp.json()
            if respj.get("requires_approval"):
                result["actions"].append({"action":"restart_service","status":"requires_manual_approval","provider_response": respj})
                result["status"] = "requires_manual_approval"
                result["notes"] = "Restart requires manual approval per policy."
            else:
                result["actions"].append({"action":"restart_service","status":"attempted","provider_response": respj})
                result["status"] = "resolved"
                result["notes"] = "Restart attempted by agent."
        except Exception as e:
            result["actions"].append({"action":"restart_service","status":"error","error": str(e)})
            result["status"] = "error"
            result["notes"] = str(e)
    else:
        # If no restart needed, maybe resolved via suggestions
        result["status"] = "no_action_needed"
        result["notes"] = "Diagnostics did not indicate an actionable automated fix."

    # save
    os.makedirs("outputs/fixes", exist_ok=True)
    with open(f"outputs/fixes/{ticket['ticket_id']}.json","w") as f:
        json.dump(result, f, indent=2)
    return result
