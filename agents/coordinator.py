# agents/coordinator.py
import json, time, os
from agents.triage_agent import triage_ticket
from agents.diagnostics_agent import run_diagnostics
from agents.fix_agent import attempt_fix
from agents.knowledge_agent import search_kb
from observability.tracing import start_trace_span


def process_ticket(ticket):
    start = time.time()
    span = start_trace_span("process_ticket", {"ticket_id": ticket.get("ticket_id")})
    try:
        # 1. Triage
        triage = triage_ticket(ticket)
        span.set_attribute("triage", triage)

        # 2. Diagnostics
        diagnostics = run_diagnostics(ticket, triage)
        span.set_attribute("diagnostics_summary", {k: (v if isinstance(v, dict) and "success" in v else "ok") for k,v in diagnostics.items() if k != "_diag_timestamp"})

        # 3. Knowledge lookup
        kb = search_kb(ticket.get("issue",""))
        span.set_attribute("kb_hits", len(kb))

        # 4. Attempt fix
        fix = attempt_fix(ticket, diagnostics)
        span.set_attribute("fix_status", fix.get("status"))

        result = {
            "ticket_id": ticket.get("ticket_id"),
            "triage": triage,
            "diagnostics": diagnostics,
            "kb": kb,
            "fix": fix,
            "processed_at": time.time()
        }
        # persist overall output
        os.makedirs("outputs", exist_ok=True)
        # write per-ticket
        with open(f"outputs/{ticket['ticket_id']}.json","w") as f:
            json.dump(result, f, indent=2)
        return result
    finally:
        span.end()
