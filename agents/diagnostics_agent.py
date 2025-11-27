# agents/diagnostics_agent.py
import requests
import os, json, time

# endpoints for simulated MCP servers
MCP_PING = "http://127.0.0.1:8001/ping"
MCP_SYSTEM_INFO = "http://127.0.0.1:8002/system_info"
MCP_LOG_SEARCH = "http://127.0.0.1:8003/search"

def run_diagnostics(ticket, triage):
    results = {}
    device = ticket.get("device_id", "unknown")
    # ping if requested
    if "ping" in triage.get("tools", []):
        try:
            resp = requests.post(MCP_PING, json={"host": device}, timeout=5)
            results["ping"] = resp.json()
        except Exception as e:
            results["ping"] = {"success": False, "error": str(e)}
    # system_info
    if "system_info" in triage.get("tools", []):
        try:
            resp = requests.post(MCP_SYSTEM_INFO, json={"device_id": device}, timeout=5)
            results["system_info"] = resp.json()
        except Exception as e:
            results["system_info"] = {"error": str(e)}
    # log_search
    if "log_search" in triage.get("tools", []):
        try:
            resp = requests.post(MCP_LOG_SEARCH, json={"device_id": device, "query": ticket.get("issue","")}, timeout=5)
            results["log_search"] = resp.json()
        except Exception as e:
            results["log_search"] = {"error": str(e)}
    # timestamp
    results["_diag_timestamp"] = time.time()
    # Save a small artifact locally (optional)
    os.makedirs("outputs/diagnostics", exist_ok=True)
    with open(f"outputs/diagnostics/{ticket['ticket_id']}.json","w") as f:
        json.dump(results, f, indent=2)
    return results
