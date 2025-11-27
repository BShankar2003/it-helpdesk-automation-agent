# agents/triage_agent.py
"""
Simple rule-based triage for PoC.
Returns category, urgency and list of suggested tools.
"""
def triage_ticket(ticket):
    text = ticket.get("issue","").lower()
    # basic rules
    if any(word in text for word in ["vpn", "network", "connect"]):
        category = "network"
        urgency = "high"
        tools = ["ping", "system_info", "log_search"]
    elif any(word in text for word in ["slow", "performance", "lag"]):
        category = "performance"
        urgency = "medium"
        tools = ["system_info", "log_search"]
    elif any(word in text for word in ["email", "sync"]):
        category = "email"
        urgency = "medium"
        tools = ["system_info", "log_search"]
    else:
        category = "general"
        urgency = "low"
        tools = ["system_info"]
    return {"category": category, "urgency": urgency, "tools": tools}
